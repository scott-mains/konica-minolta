import unittest

from api.game import Game
from api.models import Line, Point, Path
from tests.data import turns
from tests.utils import play_turn


class TestGame(unittest.TestCase):

    def test___init__(self):

        game = Game()
        self.assertEqual(game.state, 'INITIALIZE')
        self.assertIsNone(game.start_node)
        self.assertIsNone(game.end_node)
        self.assertIsNone(game.new_line)
        self.assertFalse(game.path)
        self.assertEqual(game.player, 1)

    def test__set_start_node(self):

        # verify the initial state
        game = Game()

        for i, turn in enumerate(turns):
            game(turn[0])  # receive the 1st point of the turn

            for node in game.grid.nodes:  # test all the nodes

                # verify the node was properly set or rejected

                # the node is the known valid start node from the sample turns or
                # first turn any node in the grid may be chosen as the start node
                if node == turn[0] or i == 0:

                    self.assertEqual(node, game.start_node)  # the start node is set
                    self.assertEqual(game.state, 'VALID_START_NODE')  # the state is correct

                    game(turn[1])  # finish the turn

                else:
                    self.assertIsNone(game.start_node)
                    self.assertEqual(game.state, 'INVALID_START_NODE')

    def test__set_end_node(self):
        pass

    def test__new_line(self):

        game = Game()
        for i, turn in enumerate(turns):
            play_turn(game, turn)
            self.assertEqual(game.new_line, Line(start=turn[0], end=turn[1]))

    def test__extend_path(self):
        pass

    def test__next_player(self):

        game = Game()
        for i, turn in enumerate(turns):
            play_turn(game, turn)
            self.assertEqual(game.player, 2 if i % 2 else 1)  # 0 index so player 1 is even

    def test__game_over(self):

        game = Game()
        for i, turn in enumerate(turns):
            play_turn(game, turn)
            if i < len(turns) - 1:
                self.assertFalse(game.game_over)

        self.assertTrue(game.game_over)
        self.assertEqual(game.winner, 2)


if __name__ == '__main__':
    unittest.main()
