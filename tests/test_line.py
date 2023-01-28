import unittest
from api.utils import is_horizontal, is_vertical, is_diagonal
from api.models import Line, Point


class TestLine(unittest.TestCase):

    def setUp(self) -> None:
        self.vertical = Line(start_node=Point(x=0, y=0), end_node=Point(x=0, y=3))
        self.horizontal = Line(start_node=Point(x=0, y=0), end_node=Point(x=3, y=0))
        self.diagonal = Line(start_node=Point(x=0, y=0), end_node=Point(x=3, y=3))

    def test___init___nodes_between_nodes(self):

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
