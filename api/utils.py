def is_vertical(direction: int) -> bool:
    return direction in (-90, 90, 270)


def is_horizontal(direction: int) -> bool:
    return direction in (-180, 0, 180)


def is_diagonal(direction: int) -> bool:
    return direction in (-135, -45, 45, 135, 225, 315)


def is_octilinear(direction: int) -> bool:
    return direction in (-180, -135, -90, -45, 0, 45, 90, 135, 180, 225, 270, 315)
