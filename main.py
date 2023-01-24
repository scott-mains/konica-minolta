from typing import Union

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from api.errors import InvalidStartNode

app = FastAPI()

# we add middleware to allow the client to request this api cross-origin.
# (see https://fastapi.tiangolo.com/tutorial/cors/)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # for simplicity, we allow everything
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


"""
Data Models
"""


class Point(BaseModel):
    x: int
    y: int

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


class Line(BaseModel):
    start: Point
    end: Point


class Path:
    def __init__(self):
        self._nodes = []

    @property
    def nodes(self):
        return self._nodes

    @property
    def start(self):
        try:
            return self.nodes[0]
        except IndexError:
            return None

    @property
    def end(self):
        try:
            return self.nodes[-1]
        except IndexError:
            return None

    @property
    def ends(self):
        return self.start, self.end

    def extend(self, start, end):
        index = 0 if start == self.start else -1 if start == self.end else None
        self._nodes.insert(index, end)


class StateUpdate(BaseModel):
    newline: Union[Line, None]
    heading: Union[str, None]
    message: Union[str, None]


class Payload(BaseModel):
    msg: str
    body: Union[StateUpdate, Point, str]


class Game:

    """
    Game Logic

    1. Player selects a start node.
        If this is the first node selected, any node is a valid selection,
        else the node must be either end of the path of connected nodes,
        otherwise the selected node is an invalid selection and the player must choose again.

    2. Player selects an end node.
        This node must be:
        a) adjacent or diagonal to the start node
        b) not one of the previously connected nodes on the path
        If there are no remaining valid nodes to select the game is over and the current player wins.

    """

    STATES = (
        'INITIALIZE',
        'VALID_START_NODE',
        'VALID_END_NODE',
        'GAME_OVER',
        'INVALID_START_NODE',
        'INVALID_END_NODE',
    )

    def __init__(self):
        """
        resets the game
        """
        self._state = 'INITIALIZE'
        self.grid = {Point(x=x, y=y) for x in range(4) for y in range(4)}
        # creates a set of x,y Points in a 4 x 4 grid
        # adapted from Paddy3118 in https://stackoverflow.com/questions/5450067/python-2d-array-access-with-points-x-y
        self._start_node = None
        self._end_node = None
        self.path = Path()
        self.player = 1

    def __call__(self, point: Point):
        if self.start_node is None:
            self.start_node = point
        else:
            self.end_node = point

    @property
    def state(self):
        return \
            'INITIALIZE' if self._state == 'INITIALIZE' else \
            'VALID_START_NODE' if False else \
            'VALID_END_NODE' if False else \
            'GAME_OVER' if False else \
            'INVALID_START_NODE' if False else \
            'INVALID_END_NODE' if False else \
            None
    
    @property
    def start_node(self):
        return self._start_node

    @start_node.setter
    def start_node(self, node: Point):
        choices = self.grid if self.state == 'INITIALIZE' else self.path.ends
        if node in choices:
            self._start_node = node
        else:
            raise InvalidStartNode

    @property
    def neighbors(self):
        return {}

    @property
    def end_node(self):
        return self._end_node

    @end_node.setter
    def end_node(self, node: Point):
        choices = self.neighbors
        if node in choices:
            self._end_node = node


    @property
    def new_line(self):
        if self.start_node is not None and self.end_node is not None:
            return Line(start=self.start_node, end=self.end_node)
        else:
            return None

    def next_player(self):
        self.player = 2 if self.player == 1 else 1



game = Game()

def respond(state):
    global game
    responses = {
            'VALID_START_NODE': Payload(
                msg='VALID_START_NODE',
                body=StateUpdate(
                    heading=f'Player {game.player}',
                    message=None,
                    newLine=None,
                ),
            ),
            'VALID_END_NODE': Payload(
                msg='VALID_END_NODE',
                body=StateUpdate(
                    heading=f'Player {game.player}',
                    message=None,
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
                    message='You must start on either end of the path!',
                    newLine=game.new_line,
                )
            ),
            'INVALID_END_NODE': Payload(
                msg='',
                body=StateUpdate(
                    heading='fPlayer {game.player}',
                    message='Invalid move. Try again.',
                    newline=None,
                ),
            ),
        }
    return responses[game.state]


@app.get('/initialize')
def initialize(payload: Payload):
    global game
    game = Game()
    respond()


@app.post('/node-clicked')
def on_click(point: Point):
    global game
    print('clicked:', point)
    game(point)
    respond()


@app.post('/error')
def on_error(error):
    print(error)
