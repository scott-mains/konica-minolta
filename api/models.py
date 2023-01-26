from pydantic import BaseModel, dataclasses

from .errors import PathDiscontinuity


@dataclasses.dataclass(frozen=True)  # hashable (see @antonl in https://github.com/pydantic/pydantic/issues/1303)
class Point:
    x: int
    y: int

    def __str__(self):
        return f'({self.x}, {self.y})'

    @property
    def neighbors(self):
        """
        a set of all possible neighbors.
        set of points in a 3 x 3 cartesian grid adjacent to self (except for self)
        Note: in game play edges and corners of the game grid will be excluded
        :return:
        """
        return {Point(x=self.x + i, y=self.y + j) for i in range(-1, 2) for j in range(-1, 2)} - {self}  # remove self


class Line(BaseModel):

    start: Point
    end: Point

    def __str__(self):
        return f'[{self.start}, {self.end}]'

    def crosses(self, other):
        """
        determines whether the other segment crosses this segment
        :param other: the other segment
        :return: Bool

        Two segments can cross only if:
        a) they start on the same vertical line (self.start.x == other.start.x) or
        b) they start on the same horizontal line (self.start.y == other.start.y)

        If the segments start on the same horizontal line, they cross only if:
        1. the end of the first is on the same vertical as the start of the second (self.end.x == other.start.x)
        2. the end of the second is at the same vertical as the start of the first (other.end.x == self.start.x)

        If the segments start on the same vertical line, they cross only if:
        1. the end of the first is on the same horizontal as the start of the second (self.end.x == other.start.x)
        2. the end of the second is at the same horizontal as the start of the first (other.end.x == self.start.x)
        """
        return self.start.y == other.start.y and self.end.x == other.start.x and other.end.x == self.start.x \
            or self.start.x == other.start.x and self.end.y == other.end.y and other.end.y == self.start.y


class Path:

    def __init__(self):
        self._nodes = []

    def __bool__(self):
        """
        :return: True if the path has both start and end nodes
        """
        return self.start is not None and self.end is not None

    def __str__(self):
        return f'[{", ".join(self.nodes)}]'

    @property
    def nodes(self):
        return self._nodes

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
    def ends(self):
        return self.start, self.end

    @property
    def segments(self):
        for i in range(len(self.nodes)):
            if i == 0:
                continue
            yield Line(start=self.nodes[i-1], end=self.nodes[i])

    def crosses(self, line: Line):
        """
        determines whether a new line crosses any segment of the path
        :param line:
        :return: True if the line crosses any segment of the path else False
        """
        return any((line.crosses(segment) for segment in self.segments))

    def extend(self, line: Line):
        """
        extends the path with the give line

        We extend the path by inserting the end node of the given line into the list of nodes.
        To determine whether to insert the node at the start or the end of the path, we match the start of the line to
        the start or the end of the path nodes.
        If the line is discontinuous to the path, we raise an exception to be handled by the game engine.

        :param line: the line segment to be joined to the path
        """
        index = 0 if line.start == self.start or self.start is None \
            else -1 if line.start == self.end or self.end is None \
            else None

        try:
            self._nodes.insert(index, line.end)  # insert the node at the beginning or the end of the path or raise
        except TypeError:  # index is None because the line segment is discontinuous
            raise PathDiscontinuity(f'The line {line} is discontinuous with the path:\n{self}')
            # Note: If the start and end of the new line are properly validated, this should never occur in game play
