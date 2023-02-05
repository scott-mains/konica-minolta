class Error(Exception):
    pass


class InternalError(Error):
    pass


class PlayerError(Error):
    pass


class InvalidStartNode(PlayerError):

    def __init__(self, start_node, valid_start_nodes):
        self.start_node = start_node
        self.valid_start_nodes = valid_start_nodes

    def __str__(self):
        return f'Start Node: {self.start_node} not in {self.valid_start_nodes}'


class InvalidEndNode(PlayerError):

    def __init__(self, end_node, valid_end_nodes):
        self.end_node = end_node
        self.valid_end_nodes = valid_end_nodes

    def __str__(self):
        return f'End node: {self.end_node} not in {self.valid_end_nodes}'


class InvalidLine(InternalError):

    def __init__(self, start, end, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start = start
        self.end = end

    def __str__(self):
        return f'Invalid line: [{self.start}, {self.end}]'


class PathDiscontinuity(InternalError):
    pass


class InvalidPath(InternalError):
    pass


class UnknownState(InternalError):
    pass
