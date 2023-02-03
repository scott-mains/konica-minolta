import unittest
from copy import deepcopy

from api.models import Path
from tests.data import TURNS, PATH_NODES, NEW_LINE_NODES


class TestPath(unittest.TestCase):
    def test___init__(self):
        for nodes in NEW_LINE_NODES:
            path = Path(nodes)
            self.assertListEqual(path.nodes, nodes)

    def test__extend(self):

        for i, path_nodes in enumerate(PATH_NODES):
            print(f'\nTurn {i+1}:\n')
            path = Path()
            for new_line_nodes in NEW_LINE_NODES[:i+1]:
                # print(f'new_line: {new_line_nodes}')
                other = Path(new_line_nodes)
                path.extend(other)
            print(f'path_nodes: {path.nodes} expected: {list(path_nodes)}')
            path_nodes = list(path_nodes)
            try:
                self.assertListEqual(path.nodes, list(path_nodes))
            except AssertionError:
                path_nodes.reverse()
                self.assertListEqual(path.nodes, path_nodes)


if __name__ == '__main__':
    unittest.main()
