from api.models import Grid, Line, Path, Point

# These are the Points sent in each turn in order of the sample game

turns = (
    (  # turn 1
        Point(x=0, y=0),  # note turn one could have been reversed
        Point(x=0, y=2),
    ),
    (  # turn 2
        Point(x=0, y=0),
        Point(x=1, y=0),
    ),
    (  # turn 3
        Point(x=1, y=0),
        Point(x=3, y=2),
    ),
    (  # turn 4
        Point(x=0, y=2),
        Point(x=2, y=2),
    ),
    (  # turn 5
        Point(x=3, y=2),
        Point(x=3, y=1),
    ),
    (  # turn 6
        Point(x=2, y=2),
        Point(x=3, y=3),
    ),
    (  # turn 7
        Point(x=3, y=3),
        Point(x=0, y=3),
    ),
    (  # turn 8
        Point(x=3, y=1),
        Point(x=3, y=0),
    ),
    (  # turn 9
        Point(x=3, y=0),
        Point(x=2, y=0),
    )
)


nodes = (
    (  # turn 1
        Point(x=0, y=0),  # note turn one could have been reversed
        Point(x=0, y=1),
        Point(x=0, y=2),
    ),
    (  # turn 2
        Point(x=0, y=0),
        Point(x=1, y=0),
    ),
    (  # turn 3
        Point(x=1, y=0),
        Point(x=2, y=1),
        Point(x=3, y=2),
    ),
    (  # turn 4
        Point(x=0, y=2),
        Point(x=2, y=2),
    ),
    (  # turn 5
        Point(x=3, y=2),
        Point(x=3, y=1),
    ),
    (  # turn 6
        Point(x=2, y=2),
        Point(x=3, y=3),
    ),
    (  # turn 7
        Point(x=3, y=3),
        Point(x=0, y=3),
    ),
    (  # turn 8
        Point(x=3, y=1),
        Point(x=3, y=0),
    ),
    (  # turn 9
        Point(x=3, y=0),
        Point(x=2, y=0),
    )
)