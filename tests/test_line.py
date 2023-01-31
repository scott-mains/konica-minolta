import unittest
from api.utils import is_horizontal, is_vertical, is_diagonal
from api.models import Line, Point

from tests.data import TURNS, NEW_LINE_NODES
from tests.utils import select_turns


class TestLine(unittest.TestCase):

    def setUp(self) -> None:

        self.vertical = select_turns(TURNS, 0, 7, 4)
        self.horizontal = select_turns(TURNS, 1, 3, 6, 8)
        self.diagonal = select_turns(TURNS, 2, 5)

    def test___init__(self):

        for i, (turn, nodes) in enumerate(zip(TURNS, NEW_LINE_NODES)):
            line = Line(start=turn[0], end=turn[1])
            print('turn:', i + 1, '(expected, actual)')
            for pair in zip(list(nodes), line.nodes):
                print(pair)
            self.assertListEqual(line.nodes, list(nodes))
            self.assertEqual(line.start, turn[0])
            self.assertEqual(line.end, turn[1])


if __name__ == '__main__':
    unittest.main()
