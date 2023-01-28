from tests.data import turns


def play_turn(game, turn):
    for point in turn:
        game(point)
