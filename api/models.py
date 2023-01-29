import math
from typing import Union

from pydantic.dataclasses import dataclass

from api.errors import PathDiscontinuity
from api.utils import is_octilinear


@dataclass(frozen=True)  # hashable (see @antonl in https://github.com/pydantic/pydantic/issues/1303)
class Point:
    x: int
    y: int

    def __str__(self):
        return f'({self.x}, {self.y})'

    def direction_to(self, other):
        delta_x = other.x - self.x
        delta_y = self.y - other.y  # we transpose this to account for the orientation of the grid
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
        radius = range(-self.size, self.size + 1) # e.g. [-3, -2, -1, 0, 1, 2, 3]

        for i in radius:
            for j in radius:
                node = Point(x=point.x + i, y=point.y + j)
                if node != point and Line(start=point, end=node).is_octilinear:  # skip the point in question
                    nodes.add(node)

        return nodes.intersection(self.nodes)  # remove nodes beyond the Grid


class Path:
    """
    A series of nodes defining connected line segments
    """

    def __init__(self, nodes: Union[list[Point, ...], None] = None, *args, **kwargs):
        self.nodes = [] if nodes is None else nodes  # we use a list to preserve order
        super().__init__(*args, **kwargs)

    def __bool__(self):
        """
        :return: True if the path has both start and end nodes
        """
        return self.start is not None and self.end is not None

    def __str__(self):
        return f'[{", ".join((str(node) for node in self.nodes))}]'

    def __add__(self, other):
        """
        extends this path by joining it with another

        We join the paths by inserting the end node of the given path into the list of nodes.
        To determine whether to insert the node at the start or the end of the path, we match the start of the line to
        the start or the end of the path nodes.
        If the other path is discontinuous to this path, we raise an exception to be handled by the game engine.

        Note: other path may only join from its start node to the start or end of this path and not from the other's end

        :param other: the path to be joined to the path (in Game play this will be a Line)
        """
        index = 0 if other.start == self.start or self.start is None \
            else -1 if other.start == self.end or self.end is None \
            else None

        try:
            self.nodes.insert(index, other.end)  # insert the node at the beginning or the end of the path
        except TypeError:  # index is None because the line segment is discontinuous
            raise PathDiscontinuity(f'The path {other} is discontinuous with this path:\n{self}')
            # Note: If the start and end of the new line are properly validated, this should never occur in game play

    @property
    def nodes(self) -> list[Point, ...]:
        return self._nodes

    @nodes.setter
    def nodes(self, nodes: list[Point, ...]):
        if all((isinstance(node, Point) for node in nodes)):
            self._nodes = nodes
        else:
            raise TypeError

    @property
    def start(self):
        try:
            return self.nodes[0]
        except IndexError:
            return None

    @property
    def end(self):
        try:
            return self.nodes[-1]
        except IndexError:
            return None

    @property
    def extrema(self):
        return self.start, self.end

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
        def crosses(a: Line, b: Line) -> bool:
            return a.start.y == b.start.y and a.end.x == b.start.x and b.end.x == a.start.x \
                or a.start.x == b.start.x and a.end.y == b.end.y and b.end.y == a.start.y

        return bool(set(self.nodes).intersection(set(other.nodes))) \
            or any((crosses(a, b) for a in self.segments for b in other.segments))


@dataclass
class Line(Path):
    """
    A line segment defined by a series of two or more co-linear nodes of a cartesian grid
    oriented either cardinally (0, 90, 180, 270) or ordinally (45, 135, 225, 315)
    A line segment is also a Path
    """
    def __init__(self, start: Point, end: Point, *args, **kwargs):
        x = range(start.x, end.x + 1)
        y = range(start.y, end.y + 1)
        nodes = [Point(x=start.x + i, y=start.y + j) for i in x for j in y]
        super().__init__(nodes, *args, **kwargs)

    @property
    def direction(self) -> int:
        """
        :return int: the direction in degrees from the start node to the end node
        """
        return self.start.direction_to(self.end)

    @property
    def is_octilinear(self):
        return is_octilinear(self.direction)

