import math

from pydantic import BaseModel, dataclasses

from api.errors import PathDiscontinuity


@dataclasses.dataclass(frozen=True)  # hashable (see @antonl in https://github.com/pydantic/pydantic/issues/1303)
class Point:
    x: int
    y: int

    def __str__(self):
        return f'({self.x}, {self.y})'

    @property
    def neighbors(self, radius: int = 1, direction: tuple[int] = None) -> set:
        """
        a set of neighboring points

        :param radius: limits the nodes by integer distance (x-x0, or y-y0) Default distance 1 node away
        :param direction: (optional) limits the nodes to those found between the specified direction(s)
        :return:
        """
        neighbors = set()

        for i in range(-radius, radius + 1):  # e.g. [-3, -2, -1, 0, 1, 2, 3] to find all points 3 nodes away
            for j in range(-radius, radius + 1):
                neighbor = Point(x=self.x + i, y=self.y + j)
                if Line(start_node=self, end_node=neighbor).direction in direction:
                    neighbors.add(neighbor)

        neighbors.discard(self)  # we remove this current point from the set of neighbors

        return neighbors


class Grid:
    """
    A Cartesian Grid starting at a specified point
    """
    def __init__(self, radius, origin: Point = Point(x=0, y=0)):
        self.radius = radius
        self.nodes = origin + origin.neighbors(radius=4, direction=(0, 90))



class Path:
    """
    A series of nodes defining connected line segments
    """
    def __init__(self, *args, **kwargs):
        # this is a mixin (see https://stackoverflow.com/questions/533631/what-is-a-mixin-and-why-is-it-useful)
        super().__init__(*args, **kwargs)
        self._nodes = []  # we use a list to preserve order, elsewhere in the game logic we cast as a set

    def __bool__(self):
        """
        :return: True if the path has both start and end nodes
        """
        return self.start_node is not None and self.end_node is not None

    def __str__(self):
        return f'[{", ".join(self.nodes)}]'

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
            self._nodes.insert(index, other.end_node)  # insert the node at the beginning or the end of the path
        except TypeError:  # index is None because the line segment is discontinuous
            raise PathDiscontinuity(f'The path {other} is discontinuous with this path:\n{self}')
            # Note: If the start and end of the new line are properly validated, this should never occur in game play

    @property
    def nodes(self):
        return self._nodes

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


class Line(Path, BaseModel):
    """
    A line segment defined by a series of two or more co-linear nodes of a cartesian grid
    oriented either cardinally (0, 90, 180, 270) or ordinally (45, 135, 225, 315)
    A line segment is also a Path
    """
    start: Point
    end: Point

    def __init__(self, *args, **kwargs):
        # Path is a mixin (see Path.__init__) so we only need invoke super().__init__ once
        super().__init__(*args, **kwargs)

    def __str__(self):
        return f'[{self.start}, {self.end}]'

    def direction(self):
        """
        :return: the direction in degrees
        Note: the difference along the vertical axis is transposed to account for the inversion in the game coordinates
        """
        return int(math.atan((self.start.y - self.end.y)/(self.end.x - self.start.x)) * 180 / math.pi)

    @property
    def is_octilinear(self):
        return not self.direction % 45

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
        def crosses(a, b):
            return a.start_node.y == b.start_node.y and a.end_node.x == b.start_node.x and b.end_node.x == a.start_node.x \
                or a.start_node.x == b.start_node.x and a.end_node.y == b.end_node.y and b.end_node.y == a.start_node.y

        return bool(set(self.nodes).intersection(set(other.nodes))) \
            or any((crosses() for a in self.segments for b in other.segments))
