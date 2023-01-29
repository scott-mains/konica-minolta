from api.errors import InvalidStartNode, InvalidEndNode, UnknownState
from api.models import Grid, Line, Path, Point


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
        'ERROR',
    )

    def __init__(self, grid_size=4):
        """
        resets the game
        """
        self._state = 'INITIALIZE'
        self.grid = Grid(grid_size)
        self._start_node = None
        self._end_node = None
        self._new_line = None
        self.path = Path()
        self.player = 1
        self.error = None

    def __call__(self, point: Point):

        try:
            if self.start_node is None:
                try:
                    self.start_node = point
                    self.state = 'VALID_START_NODE'
                except InvalidStartNode:
                    self.state = 'INVALID_START_NODE'
            else:
                try:
                    self.end_node = point
                    self.path += self.new_line
                    self.state = 'VALID_END_NODE' if not self.game_over else 'GAME_OVER'
                    self.next_player()
                except InvalidEndNode:
                    self.state = 'INVALID_END_NODE'

        except Exception as e:
            self.error = str(e)
            self.state = 'ERROR'
            raise e  # for debugging  todo: comment when done

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, state):
        if state in self.STATES:
            self._state = state
        else:
            raise UnknownState

    @property
    def start_node(self):
        return self._start_node

    @start_node.setter
    def start_node(self, node: Point):
        # on the first turn all nodes are valid start nodes.
        # once the first path segment has been defined, subsequent segments must start on either end of the path
        choices = self.grid.nodes if self.state == 'INITIALIZE' else self.path.extrema
        if node in choices or node is None:
            self._start_node = node
        else:
            self._start_node = None
            raise InvalidStartNode

    @property
    def end_node(self):
        return self._end_node

    @end_node.setter
    def end_node(self, node: Point):
        if node in self.valid_end_nodes(self.start_node) or node is None:
            self._end_node = node
        else:
            raise InvalidEndNode

    def valid_end_nodes(self, start_node: Point):
        """
        :return: set of Points that would define Line that is octilinear to and does not intersect the current path

        This method is called by:
         a) the end_node setter to determine if the selected point is a valid end node
         b) the game_over property to determine if the game is over, i.e. neither the start nor the end of the path has
            any valid end nodes.
        """
        # if not isinstance(start_node, Point):
        #     raise TypeError(f'Start node is type: {type(start_node)}.  Expected a Point')

        return {
            node for node in self.grid.nodes_octilinear_to(start_node)
            if not self.path.intersects(Line(end=node, start=start_node))
        }

    @property
    def new_line(self):

        if self.start_node is not None and self.end_node is not None:
            return Line(start=self.start_node, end=self.end_node)
        else:
            return None

    def next_player(self):
        if self.new_line is not None:  # a line has been completed. it is now the other player's turn
            self.player = 2 if self.player == 1 else 1
        self.end_node = self.start_node = None

    @property
    def game_over(self):
        """
        The game is over if neither the start nor the end of the path has any valid end nodes.
        :return: bool
        """
        return True \
            if self.path and not self.valid_end_nodes(self.path.start) and not self.valid_end_nodes(self.path.end) \
            else False

    @property
    def winner(self):
        return self.player if self.game_over else None
