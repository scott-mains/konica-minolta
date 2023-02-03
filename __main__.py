from typing import Union

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pydantic.dataclasses import dataclass

from api.game import Game
from api.models import Point, Line

app = FastAPI()

# add middleware to allow the client to request this api cross-origin without access control headers
# see https://fastapi.tiangolo.com/tutorial/cors/
app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_methods=['*'], expose_headers=['*'])

game = Game()


@dataclass
class StateUpdate:
    newLine: Union[Line, None] = None
    heading: Union[str, None] = None
    message: Union[str, None] = None


@dataclass
class Payload:
    msg: str
    body: Union[StateUpdate, Point, str]


@dataclass
class Error:
    error: str

    def __str__(self):
        return self.error


def respond() -> Payload:

    match game.state:

        case 'INITIALIZE':
            response = Payload(
                msg='INITIALIZE',
                body=StateUpdate(
                    heading=f'Player {game.player}',
                    message=f'Awaiting Player {game.player}\'s Move',
                    newLine=None,
                ),
            )

        case 'VALID_START_NODE':
            response = Payload(
                msg='VALID_START_NODE',
                body=StateUpdate(
                    heading=f'Player {game.player}',
                    message="Select a second node to complete the line.",
                    newLine=None,
                ),
            )

        case 'VALID_END_NODE':
            response = Payload(
                msg='VALID_END_NODE',
                body=StateUpdate(
                    heading=f'Player {game.player}',
                    message=f'Awaiting Player {game.player}\'s Move',
                    newLine=game.new_line,
                ),
            )

        case 'GAME_OVER':
            response = Payload(
                msg='GAME_OVER',
                body=StateUpdate(
                    heading='Game Over',
                    message=f'Player {game.winner} wins!',
                    newLine=game.new_line,
                )
            )

        case 'INVALID_START_NODE':
            response = Payload(
                msg='INVALID_START_NODE',
                body=StateUpdate(
                    heading=f'Player {game.player}',
                    message='''
                    Invalid start position.
                    You must start at either end of the path.
                    Try again.
                    ''',
                    newLine=None,
                )
            )

        case 'INVALID_END_NODE':
            response = Payload(
                msg='INVALID_END_NODE',
                body=StateUpdate(
                    heading=f'Player {game.player}',
                    message='''
                    Invalid end position.
                    You must choose a node in an octilinear direction that does not intersect the path.
                    Try again.
                    ''',
                    newline=None,
                ),
            )

        case 'ERROR':
            response = Payload(
                msg='ERROR',
                body=StateUpdate(
                    heading='Error',
                    message=game.error,
                    newLine=None,
                ),
            )

        case _:
            response = Payload(
                msg=game.state,
                body=StateUpdate(
                    heading=game.state,
                    message=game.state,
                    newLine=None
                )
            )

    print(response)
    return response


@app.get('/initialize', response_model=Payload)
def initialize():
    global game
    game = Game()
    return respond()


@app.post('/node-clicked', response_model=Payload)
def on_click(point: Point):
    print('clicked:', point)
    game(point)
    return respond()


@app.post('/error', response_model=Payload)
def on_error(error: Error):
    game.error = str(error)
    game.state = 'ERROR'
    return respond()  # this response will be ignored by the client, but it must be sent


if __name__ == '__main__':
    uvicorn.run(app)
