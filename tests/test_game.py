import unittest

from api.game import Game
from api.models import Line, Point, Path
from tests.data import TURNS, VALID_END_NODES, VALID_START_NODES
from tests.utils import play_turn


class TestGame(unittest.TestCase):

    def test___init__(self):

        game = Game()
        self.assertEqual(game.state, 'INITIALIZE')
        self.assertIsNone(game.start_node)
        self.assertIsNone(game.end_node)
        self.assertIsNone(game.new_line)
        self.assertIsNotNone(game.path)
        self.assertFalse(game.path)
        self.assertEqual(game.player, 1)

    def test__set_start_node(self):

        print('(expected, actual)')
        for node in Game().grid.nodes:  # test all the nodes
            for i in range(len(TURNS) + 1):  # through all the turns in the sample game  todo: use a fixture
                game = Game()  # Initialize the game
                for turn in TURNS[:i]:
                    play_turn(game, turn)  # play the game until the turn in question
                game(node)  # receive the next node

                print('Turn:', i + 1)
                print('node:', node, game.start_node)
                print('state:', 'VALID_START_NODE' if node in VALID_START_NODES[i] else 'INVALID_START_NODE', game.state)

                # if node in VALID_START_NODES[i]:  # known valid start nodes
                #     self.assertEqual(node, game.start_node)  # the start node is set
                #     self.assertEqual(game.state, 'VALID_START_NODE')  # the state is correct
                # else:
                #     self.assertIsNone(game.start_node)  # the node is not set
                #     self.assertEqual(game.state, 'INVALID_START_NODE') # the state is correct

    def test__set_end_node(self):

        for node in Game().grid.nodes:  # test all the nodes
            for i in range(len(TURNS)):  # through all the turns in the sample game  todo: use a fixture
                game = Game()  # Initialize the game
                for turn in TURNS[:i]:
                    play_turn(game, turn)  # play the game until the turn in question
                game(TURNS[i][0])  # set the start node of the present turn
                game(node)  # receive the next end node

                # assertions
                if node in VALID_END_NODES[i]:  # known valid end nodes for the present turn
                    self.assertEqual(node, game.start_node)  # the start node is set
                    self.assertEqual(game.state, 'VALID_START_NODE')  # the state is correct
                else:
                    self.assertIsNone(game.start_node)  # the node is not set
                    self.assertEqual(game.state, 'INVALID_START_NODE')  # the state is correct

    def test__new_line(self):

        # verify all the new lines of the sample game are represented properly
        game = Game()
        for i, turn in enumerate(TURNS):
            play_turn(game, turn)
            self.assertEqual(game.new_line, Line(start=turn[0], end=turn[1]))

        game = Game()
        play_turn(TURNS[0])
        invalid_start_node = Point(x=3, y=3)
        game(invalid_start_node)
        self.assertIsNone(game.new_line)

    def test__next_player(self):

        game = Game()
        for i, turn in enumerate(TURNS):
            play_turn(game, turn)
            self.assertEqual(game.player, 2 if i % 2 else 1)  # 0 index so player 1 is even
            self.assertIsNone(game.start_node)
            self.assertIsNone(game.end_node)
            self.assertIsNotNone(self.path)

    def test__game_over(self):

        game = Game()
        for i, turn in enumerate(TURNS):
            play_turn(game, turn)
            if i < len(TURNS) - 1:
                self.assertFalse(game.game_over)

        self.assertTrue(game.game_over)
        self.assertEqual(game.winner, 2)


if __name__ == '__main__':
    unittest.main()
