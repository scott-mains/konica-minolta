import unittest
from api.utils import is_horizontal, is_vertical, is_diagonal
from api.models import Line, Point

from tests.data import turns
from tests.utils import select_turns


class TestLine(unittest.TestCase):

    def setUp(self) -> None:

        self.vertical = select_turns(0, 8, 5)
        self.horizontal = select_turns(1, 3, 6, 8)
        self.diagonal = select_turns()

    def test___init__(self):

        for turn in self.vertical:
            line = Line(start=turn[0], end=turn[1])
            self.assertEqual(line.start_node, turn[0])
            self.assertEqual(line.start_node, turn[1])
            self.assertListEqual(line.nodes, )

        # vertical
        self.assertListEqual(
            self.vertical.nodes, [
                Point(x=0, y=0),
                Point(x=0, y=1),
                Point(x=0, y=2),
                Point(x=0, y=3),
            ]
        )

        # horizontal
        self.assertListEqual(
            self.horizontal.nodes, [
                Point(x=0, y=0),
                Point(x=1, y=0),
                Point(x=2, y=0),
                Point(x=3, y=0),
            ]
        )

        # diagonal
        self.asserListEqual(
            self.diagonal.nodes, [
                Point(x=0, y=0),
                Point(x=1, y=1),
                Point(x=2, y=2),
                Point(x=3, y=3),
            ]
        )

    def test__direction(self):
        self.assertTrue(is_vertical(self.vertical.direction))
        self.assertTrue(is_horizontal(self.horizontal.direction))
        self.assertTrue(is_diagonal(self.diagonal.direction))


if __name__ == '__main__':
    unittest.main()
