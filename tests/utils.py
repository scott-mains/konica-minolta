from tests.data import TURNS


def select_turns(*indices: [int, ...]):
    return tuple(turn for turn in filter(lambda i: i in indices, TURNS))


def play_turn(game, turn):
    for point in turn:
        game(point)
