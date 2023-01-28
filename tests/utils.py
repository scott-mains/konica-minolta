from tests.data import turns


def select_turns(*indices: [int, ...]):
    return filter(lambda i: i in indices, turns)


def play_turn(game, turn):
    for point in turn:
        game(point)
