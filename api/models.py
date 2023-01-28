import math
from typing import Union
from pydantic import BaseModel, dataclasses, Field

from api.errors import PathDiscontinuity
from api.utils import is_octilinear


@dataclasses.dataclass(frozen=True)  # hashable (see @antonl in https://github.com/pydantic/pydantic/issues/1303)
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
                if node != point and Line(start_node=point, end_node=node).is_octilinear:  # skip the point in question
                    nodes.add(node)

        return nodes.intersection(self.nodes)  # remove nodes beyond the Grid


class Path:
    """
    A series of nodes defining connected line segments
    """

    def __init__(self, nodes: Union[list[Point, ...], None] = None, *args, **kwargs):

        # this is a mixin (see https://stackoverflow.com/questions/533631/what-is-a-mixin-and-why-is-it-useful)
        super().__init__(*args, **kwargs)
        self.nodes = [] if nodes is None else nodes  # we use a list to preserve order

    def __bool__(self):
        """
        :return: True if the path has both start and end nodes
        """
        return self.start_node is not None and self.end_node is not None

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
        index = 0 if other.start_node == self.start_node or self.start_node is None \
            else -1 if other.start_node == self.end_node or self.end_node is None \
            else None

        try:
            self.nodes.insert(index, other.end_node)  # insert the node at the beginning or the end of the path
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
    def start_node(self):
        try:
            return self.nodes[0]
        except IndexError:
            return None

    @property
    def end_node(self):
        try:
            return self.nodes[-1]
        except IndexError:
            return None

    @property
    def extrema(self):
        return self.start_node, self.end_node

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
            return a.start_node.y == b.start_node.y and a.end_node.x == b.start_node.x and b.end_node.x == a.start_node.x \
                or a.start_node.x == b.start_node.x and a.end_node.y == b.end_node.y and b.end_node.y == a.start_node.y

        return bool(set(self.nodes).intersection(set(other.nodes))) \
            or any((crosses(a, b) for a in self.segments for b in other.segments))


# @dataclasses.dataclass(frozen=True)
class Line(Path, BaseModel):
    """
    A line segment defined by a series of two or more co-linear nodes of a cartesian grid
    oriented either cardinally (0, 90, 180, 270) or ordinally (45, 135, 225, 315)
    A line segment is also a Path
    """
    start: Point
    end: Point

    # we overload the __init__ to make use of pydantic BaseModel field validation while subclassing from the Path mixin
    def __init__(self, *args, **kwargs):
        # Path is a mixin (see Path.__init__) so we only need invoke super().__init__ once
        super().__init__(*args, **kwargs)
        direction = start_node.direction_to(end_node)

        x = range(self.start.x, self.end.x + 1)
        y = range(self.start.y, self.end.y + 1)

        nodes = [Point(x=start.x + i, y=start_node.y + j) for i in x for j in y]

        self.nodes = nodes

    @property
    def direction(self) -> int:
        """
        :return int: the direction in degrees from the start node to the end node
        """
        return self.start_node.direction_to(self.end_node)

    @property
    def is_octilinear(self):
        return is_octilinear(self.direction)

