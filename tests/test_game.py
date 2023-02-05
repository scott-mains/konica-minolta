import unittest

from api.game import Game
from api.models import Line, Point, Path
from api.errors import InvalidStartNode, InvalidEndNode
from tests.data import TURNS, PATH_NODES, VALID_END_NODES, VALID_START_NODES
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

        for i in range(len(TURNS)):  # test all the turns in the sample game  todo: use a fixture
            print(f'\nTurn {i + 1}:\n')  # test turn
            valid_start_nodes = VALID_START_NODES[i]  # fixture of known valid start nodes for this turn
            print('Valid start nodes:', valid_start_nodes)
            for node in Game().grid.nodes:  # test all the nodes
                print('\nnode:', node, '\n')  # present test node
                game = Game()  # Initialize the game
                for turn in TURNS[:i]:
                    play_turn(game, turn)  # play the game up until the turn in question

                  # play the test node as the start node of the turn in question

                # evaluate
                if node in valid_start_nodes:
                    game.start_node = node
                    print(f'start_node: {game.start_node} expected: {node}')
                    self.assertEqual(node, game.start_node)  # the start node is set
                else:
                    with self.assertRaises(InvalidStartNode):
                        try:
                            game.start_node = node # the node is not set
                        except InvalidStartNode as e:
                            print(f'start_node: {node} expected: {e}')
                            raise

    def test__set_end_node(self):

        for i in range(len(TURNS)):  # through all the turns in the sample game  todo: use a fixture
            print(f'\nTurn {i + 1}:\n')  # test turn
            start_node = TURNS[i][0]
            print(f'start_node: {start_node}\n')
            valid_end_nodes = VALID_END_NODES[i]
            print(f'Valid end nodes: {valid_end_nodes}\n')

            for node in Game().grid.nodes:  # test all the nodes
                print(f'\nnode: {node}\n')
                game = Game()  # Initialize the game
                for turn in TURNS[:i]:
                    play_turn(game, turn)  # play the game until the turn in question
                game(start_node)  # set the start node of the present turn
                print(f'path: {str(game.path)}\n')
                # assertions
                if node in valid_end_nodes:  # known valid end nodes for the present turn
                    game.end_node = node  # receive the next end node
                    print(f'end_node: {game.end_node} expected: {node}')
                    self.assertEqual(node, game.end_node)  # the start node is set
                else:
                    with self.assertRaises(InvalidEndNode):
                        try:
                            game.end_node = node  # the node is invalid
                        except InvalidEndNode as e:
                            print(f'expected: {e}')
                            raise

    def test__new_line(self):

        # verify all the new lines of the sample game are represented properly
        game = Game()
        for i, turn in enumerate(TURNS):
            print(f'\nTurn: {i+1}')
            play_turn(game, turn)
            new_line = Line(start=turn[0], end=turn[1])
            print(f'new_line: {game.new_line} expected: {new_line}')
            self.assertEqual(game.new_line, new_line)

    def test__next_player(self):

        game = Game()
        for i, turn in enumerate(TURNS):
            print(f'\nTurn {i + 1}')
            play_turn(game, turn)
            self.assertEqual(game.player, 2 if i % 2 == 0 else 1)  # 0 index so player 1 is even
            self.assertIsNone(game.start_node)
            self.assertIsNone(game.end_node)
            self.assertIsNotNone(game.path)

    def test__game_over(self):
        game = Game()
        for i, turn in enumerate(TURNS):
            print(f'\nTurn {i+1}')
            play_turn(game, turn)
            if i < len(TURNS) - 1:
                print(f'game_over: {game.game_over} Expected: False')
                print(f'winner: {game.winner} Expected: None')
                self.assertFalse(game.game_over)
                self.assertIsNone(game.winner)
            else:
                print(f'state: {game.state} Expected: GAME_OVER')
                print(f'winner: {game.winner} Expected: 2')
                # self.assertTrue(game.game_over)
                self.assertEqual('GAME_OVER', game.state)
                self.assertEqual(game.winner, 2)


if __name__ == '__main__':
    unittest.main()
