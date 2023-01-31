class Error(Exception):
    pass


class InternalError(Error):
    pass


class PlayerError(Error):
    pass


class InvalidStartNode(PlayerError):
    pass


class InvalidEndNode(PlayerError):
    pass


class InvalidLine(InternalError):

    def __init__(self, start, end, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start = start
        self.end = end

    def __str__(self):
        return f'Invalid line: [{self.start}, {self.end}]'


class PathDiscontinuity(InternalError):
    pass


class UnknownState(InternalError):
    pass
