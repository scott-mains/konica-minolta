from api.models import Grid, Line, Path, Point

# These are the Points sent in each turn in order of the sample game

TURNS = (
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

NEW_LINE_NODES = (
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
        Point(x=1, y=2),
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
        Point(x=2, y=3),
        Point(x=1, y=3),
        Point(x=0, y=3),
    ),
    (  # turn 8
        Point(x=3, y=1),
        Point(x=3, y=0),
    ),
    (  # turn 9
        Point(x=3, y=0),
        Point(x=2, y=0),
    ),
)

PATH_NODES = (
    (  # turn 1
        Point(x=0, y=0),
        Point(x=0, y=1),
        Point(x=0, y=2),
    ),
    (  # turn 2
        Point(x=1, y=0),
        Point(x=0, y=0),
        Point(x=0, y=1),
        Point(x=0, y=2),
    ),
    (  # turn 3
        Point(x=0, y=2),
        Point(x=0, y=1),
        Point(x=0, y=0),
        Point(x=1, y=0),
        Point(x=2, y=1),
        Point(x=3, y=2),
    ),
    (  # turn 4
        Point(x=2, y=2),
        Point(x=1, y=2),
        Point(x=0, y=2),
        Point(x=0, y=1),
        Point(x=0, y=0),
        Point(x=1, y=0),
        Point(x=2, y=1),
        Point(x=3, y=2),
    ),
    (  # turn 5
        Point(x=2, y=2),
        Point(x=1, y=2),
        Point(x=0, y=2),
        Point(x=0, y=1),
        Point(x=0, y=0),
        Point(x=1, y=0),
        Point(x=2, y=1),
        Point(x=3, y=2),
        Point(x=3, y=1),
    ),
    (  # turn 6
        Point(x=3, y=3),
        Point(x=2, y=2),
        Point(x=1, y=2),
        Point(x=0, y=2),
        Point(x=0, y=1),
        Point(x=0, y=0),
        Point(x=1, y=0),
        Point(x=2, y=1),
        Point(x=3, y=2),
        Point(x=3, y=1),

    ),
    (  # turn 7
        Point(x=0, y=3),
        Point(x=1, y=3),
        Point(x=2, y=3),
        Point(x=3, y=3),
        Point(x=2, y=2),
        Point(x=1, y=2),
        Point(x=0, y=2),
        Point(x=0, y=1),
        Point(x=0, y=0),
        Point(x=1, y=0),
        Point(x=2, y=1),
        Point(x=3, y=2),
        Point(x=3, y=1),
    ),
    (  # turn 8
        Point(x=0, y=3),
        Point(x=1, y=3),
        Point(x=2, y=3),
        Point(x=3, y=3),
        Point(x=2, y=2),
        Point(x=1, y=2),
        Point(x=0, y=2),
        Point(x=0, y=1),
        Point(x=0, y=0),
        Point(x=1, y=0),
        Point(x=2, y=1),
        Point(x=3, y=2),
        Point(x=3, y=1),
        Point(x=3, y=0),
    ),
    (  # turn 9
        Point(x=0, y=3),
        Point(x=1, y=3),
        Point(x=2, y=3),
        Point(x=3, y=3),
        Point(x=2, y=2),
        Point(x=1, y=2),
        Point(x=0, y=2),
        Point(x=0, y=1),
        Point(x=0, y=0),
        Point(x=1, y=0),
        Point(x=2, y=1),
        Point(x=3, y=2),
        Point(x=3, y=1),
        Point(x=3, y=0),
        Point(x=2, y=0),
    ),
)

VALID_START_NODES = (
    Grid().nodes,  # turn 1, all nodes are available
    {   # turn 2
        Point(x=0, y=0),  # start
        Point(x=0, y=2),  # end
    },
    {   # turn 3
        Point(x=0, y=2),
        Point(x=1, y=0),
    },
    {   # turn 4
        Point(x=0, y=2),
        Point(x=3, y=2),
    },
    {   # turn 5
        Point(x=2, y=2),
        Point(x=3, y=2),
    },
    {   # turn 6
        Point(x=2, y=2),
        Point(x=3, y=1),
    },
    {   # turn 7
        Point(x=3, y=3),
        Point(x=3, y=1),
    },
    {   # turn 8
        Point(x=0, y=3),  # VALID_START_NODE per rules but no VALID_END_NODE in ths scenario
        Point(x=3, y=1),
    },
    {   # turn 9
        Point(x=0, y=3),
        Point(x=3, y=0),
    },
)

VALID_END_NODES = (

    # turn 1
    # start: Point(x=0, y=0),
    {
        # down
        Point(x=0, y=1),
        Point(x=0, y=2),
        Point(x=0, y=3),

        # down right
        Point(x=1, y=1),
        Point(x=2, y=2),
        Point(x=3, y=3),

        # right
        Point(x=1, y=0),
        Point(x=2, y=0),
        Point(x=3, y=0),

    },

    # turn 2
    # start: Point(x=0, y=0),
    {
        # down right
        Point(x=1, y=1),
        Point(x=2, y=2),
        Point(x=3, y=3),
        # right
        Point(x=1, y=0),
        Point(x=2, y=0),
        Point(x=3, y=0),
    },

    # turn 3
    # start: Point(x=1, y=0)
    {
        # down
        Point(x=1, y=1),
        Point(x=1, y=2),
        Point(x=1, y=3),
        # down right
        Point(x=1, y=0),
        Point(x=2, y=1),
        Point(x=3, y=2),
        # right
        Point(x=2, y=0),
        Point(x=3, y=0),
    },

    # turn 4
    # Point(x=0, y=2)
    {
        # right
        Point(x=1, y=2),
        Point(x=2, y=2),
        Point(x=3, y=2),
        # up right
        Point(x=1, y=1),
        Point(x=2, y=2),
        # down
        Point(x=3, y=2),
        # down right
        Point(x=1, y=3),
    },

    # turn 5
    # Point(x=3, y=2)
    {
        # up
        Point(x=3, y=0),
        Point(x=3, y=1),
        # down
        Point(x=3, y=3),
        # down left
        Point(x=2, y=3)
    },

    # turn 6
    # Point(x=2, y=2),
    {
        # down
        Point(x=2, y=3),
        # down left
        Point(x=1, y=3),
        # down right
        Point(x=3, y=3),
        # up left
        Point(x=1, y=1)
    },

    # turn 7
    # Point(x=3, y=3),
    {
        # left
        Point(x=2, y=3),
        Point(x=1, y=3),
        Point(x=0, y=3),
    },

    # turn 8
    # Point(x=3, y=1),
    {
        # up
        Point(x=3, y=0),
        # up left
        Point(x=2, y=0),
    },

    # turn 9
    # Point(x=3, y=0)
    {
        # left
        Point(x=2, y=0),
    },
)
