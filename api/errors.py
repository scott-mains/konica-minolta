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


class PathDiscontinuity(InternalError):
    pass
