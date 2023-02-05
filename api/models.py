import math
from copy import copy
from typing import Union

from pydantic.dataclasses import dataclass

from api.errors import PathDiscontinuity, InvalidLine, InvalidPath
from api.utils import is_octilinear, is_horizontal, is_diagonal, is_vertical


@dataclass(frozen=True)  # hashable (see @antonl in https://github.com/pydantic/pydantic/issues/1303)
class Point:
    x: int
    y: int

    def __str__(self):
        return f'({self.x}, {self.y})'

    def direction_to(self, other):
        delta_x = other.x - self.x
        delta_y = other.y - self.y
        return int(round(math.atan2(delta_y, delta_x) * 180 / math.pi))


class Grid:
    """
    A Cartesian Grid starting at a specified point
    """
    def __init__(self, size=4):
        self.size = size
        self.nodes = {Point(x=i, y=j) for i in range(size) for j in range(size)}
        # creates a set of x,y Points in a 4 x 4 grid
        # adapted from Paddy3118 in https://stackoverflow.com/questions/5450067/python-2d-array-access-with-points-x-y

    def nodes_octilinear_to(self, point: Point) -> set[Point, ...]:
        '''
        determines which nodes in the grid would form an octilinear line with the given point
        :return nodes: the set of nodes
        '''

        nodes = set()  # container for the node

        # we set a search radius up to the size of the grid in both directions
        radius = range(-self.size, self.size + 1)  # e.g. [-3, -2, -1, 0, 1, 2, 3]

        for i in radius:
            for j in radius:
                node = Point(x=point.x + i, y=point.y + j)
                if node != point and is_octilinear(point.direction_to(node)):  # skip the original point
                    nodes.add(node)

        return nodes.intersection(self.nodes)  # remove nodes beyond the Grid


class Path:
    """
    A series of nodes defining connected line segments
    this is also considered a "directed graph" (see https://www.redblobgames.com/pathfinding/grids/graphs.html)
    """

    def __init__(self, nodes: Union[list[Point, ...], None] = None, *args, **kwargs):
        self.nodes = nodes

    def __bool__(self):
        """
        :return: True if the path has both start and end nodes
        """
        return bool(self.nodes)

    def __str__(self):
        return f'[{", ".join((str(node) for node in self.nodes))}]'

    def extend(self, other):
        """
        extends this path by joining it with another

        We join the paths by inserting the end node of the given path into the list of nodes.
        To determine whether to insert the node at the start or the end of the path, we match the start of the line to
        the start or the end of the path nodes.
        If the other path is discontinuous to this path, we raise an exception to be handled by the game engine.

        Note: other path may only join from its start node to the start or end of this path and not from the other's end

        :param other: the path to be joined to the path (in Game play this will be a Line)
        """
        self_nodes = list(self.nodes)
        other_nodes = list(other.nodes)  # we recast to new list to avoid mutating the other path, also force to list

        if not self:  # this path has no nodes yet
            self.nodes = other_nodes  # we just use the other's nodes

        elif other._start == self._end:
            self_nodes.pop()  # remove the end
            self_nodes.extend(other_nodes)
            self.nodes = self_nodes

        elif other._start == self._start:
            other_nodes.reverse()
            other_nodes.pop()
            other_nodes.extend(self_nodes)
            self.nodes = other_nodes

        else:
            raise PathDiscontinuity(f'The path {other} is discontinuous with this path:\n{self}')
            # Note: If the start and end of the new line are properly validated, this should never occur in game play

    @property
    def nodes(self) -> list[Point, ...]:
        return self._nodes

    @nodes.setter
    def nodes(self, nodes: list[Point, ...]):
        if nodes is None:
            self._nodes = []
        elif all((isinstance(node, Point) for node in nodes)):
            self._nodes = list(nodes)  # recast as list to avoid mutating source in later operations
        else:
            raise TypeError

    @property
    def _start(self):
        """
        todo: there is some redundancy here due to pydantic field name collision so we make this protected and read only
        """
        try:
            return self.nodes[0]
        except IndexError:
            raise AttributeError

    @property
    def _end(self):
        try:
            return self.nodes[-1]
        except IndexError:
            raise AttributeError

    @property
    def extrema(self):
        """
        this property is used in Game play to determine whether a start node is valid,
        i.e. it is one of the path ends

        :return:
        """
        return self._start, self._end

    @property
    def segments(self):
        for i in range(len(self.nodes)):
            if i == 0:
                continue
            yield Line(start=self.nodes[i-1], end=self.nodes[i])

    def intersects(self, other):
        """
        determines whether this line (i.e. any of its segments or nodes) intersects the other line's segments or nodes
        :param other: the other line
        :return: Bool

        A line intersects another either at a node, or by crossing segments between nodes:
        1. Intersection at a node occurs where any node of this line is coincident with any node of the other line.
        2. Intersection by crossing occurs where segments starts at the same vertical and the start of the first and the
        end of the second are on the same horizontal and vice versa
        """
        def _crosses(a: Line, b: Line) -> bool:

            if not a and not b:
                return False

            if not is_diagonal(a.direction) or not is_diagonal(b.direction):
                return False

            if abs(a.direction - b.direction) != 90:
                return False

            if a._start.y == b._start.y:

                if not abs(a._start.x - b._start.x) == abs(a._end.x - b._end.x) == 1:
                    return False

                return a._end.x == b._start.x and b._end.x == a._start.x

            if a._start.x == b._start.x:

                if not abs(a._start.y - b._start.y) == abs(a._end.y - b._end.y) == 1:
                    return False

                return a._end.y == b._start.y and b._end.y == a._start.y

        if not self:
            return False

        self_nodes = list(self.nodes)
        other_nodes = list(other.nodes)

        if other._start == self._end:
            self_nodes.pop()

        elif other._start == self._start:
            other_nodes.reverse()  # in this case the other nodes will be reversed
            other_nodes.pop()

        intersects = bool(set(self_nodes).intersection(set(other_nodes)))

        crosses = [_crosses(a, b) for a in self.segments for b in other.segments]

        return intersects or any(crosses)


@dataclass
class Line(Path):
    """
    A special case of a Path
    An octilinear line segment defined by a series of two or more co-linear nodes of a cartesian grid
    oriented either cardinally (0, 90, 180, 270) or ordinally (45, 135, 225, 315)
    """
    start: Point
    end: Point

    def __init__(self, *args, **kwargs):
        start, end = kwargs.get('start'), kwargs.get('end')

        if start is None or end is None:  # we have to allow None to comply with pydantic field validation
            raise InvalidLine(start, end)  # but the line is invalid

        if not is_octilinear(start.direction_to(end)):
            raise InvalidLine(start, end)  # the line is not allowed in this game because it is not octilinear

        # Since a Line is a special octilinear case of a path, we fill in the nodes between the start and end,
        # starting with the start node, we add nodes increasing x and y by a delta we increment until we reach the end.

        delta_x = end.x - start.x
        delta_y = end.y - start.y

        if delta_x == 0 and delta_y == 0:
            raise InvalidLine(start, end)

        if delta_x > 0:
            deltas_x = list(range(0, delta_x + 1))

        if delta_y > 0:
            deltas_y = list(range(0, delta_y + 1))

        if delta_x < 0:
            deltas_x = list(range(delta_x, 1))
            deltas_x.reverse()  # we reverse the deltas to match the sense

        if delta_y < 0:
            deltas_y = list(range(delta_y, 1))
            deltas_y.reverse()

        if delta_y == 0:
            deltas_y = [0] * len(deltas_x)

        if delta_x == 0:
            deltas_x = [0] * len(deltas_y)

        nodes = [
            Point(x=start.x + delta_x, y=start.y + delta_y)
            for delta_x, delta_y in zip(deltas_x, deltas_y)
        ]

        super().__init__(nodes)
        try:
            self.start = copy(self.extrema[0])
            self.end = copy(self.extrema[1])
        except AttributeError:
            self.start = None
            self.end = None
            raise InvalidLine(self.start, self.end)

    @property
    def direction(self) -> int:
        """
        :return int: the direction in degrees from the start node to the end node
        """
        return self.start.direction_to(self.end)
