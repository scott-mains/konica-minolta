from typing import Union

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from api.game import Game
from api.models import Point, Line

app = FastAPI()

# add middleware to allow the client to request this api cross-origin without access control headers
# see https://fastapi.tiangolo.com/tutorial/cors/
app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_methods=['*'], expose_headers=['*'])

global game
game = Game()


class StateUpdate(BaseModel):
    newline: Union[Line, None]
    heading: Union[str, None]
    message: Union[str, None]


class Payload(BaseModel):
    msg: str
    body: Union[StateUpdate, Point, str]


class Error(BaseModel):
    error: str

    def __str__(self):
        return self.error


def respond() -> Payload:
    return {
        'INITIALIZE': Payload(
            msg='INITIALIZE',
            body=StateUpdate(
                heading=f'Player {game.player}',
                message=f'Awaiting Player {game.player}\'s Move',
                newLine=None
            ),

        ),
        'VALID_START_NODE': Payload(
            msg='VALID_START_NODE',
            body=StateUpdate(
                heading=f'Player {game.player}',
                message="Select a second node to complete the line.",
                newLine=None,
            ),
        ),
        'VALID_END_NODE': Payload(
            msg='VALID_END_NODE',
            body=StateUpdate(
                heading=f'Player {game.player}',
                message=f'Awaiting Player {game.player}\'s Move',
                newLine=game.new_line,
            ),
        ),
        'GAME_OVER': Payload(
            msg='GAME_OVER',
            body=StateUpdate(
                heading='Game Over',
                message=f'Player {game.player} wins!',
                newLine=game.new_line,
            )
        ),
        'INVALID_START_NODE': Payload(
            msg='INVALID_START_NODE',
            body=StateUpdate(
                heading=f'Player {game.player}',
                message='''
                Invalid start position.
                You must start at either end of the path.
                Try again.
                ''',
                newLine=game.new_line,
            )
        ),
        'INVALID_END_NODE': Payload(
            msg='INVALID_END_NODE',
            body=StateUpdate(
                heading=f'Player {game.player}',
                message='''
                Invalid end position.
                You must choose a neighboring node that does not intersect the path.
                Try again.
                ''',
                newline=None,
            ),
        ),
        'ERROR': Payload(
            msg='ERROR',
            body=StateUpdate(
                heading='Error',
                message=game.error,
                newLine=None,
            ),
        ),
    }[game.state]


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
    print(error)
    game.error = str(error)
    game.state = 'ERROR'
    return respond()  # this response will be ignored by the client, but it must be sent


if __name__ == '__main__':
    uvicorn.run(app)
