# config.py
# All game settings in one place (NFR 5.6.1).

# Players and pieces
MIN_PLAYERS = 2
MAX_PLAYERS = 4
PIECES_PER_PLAYER = 4
MAX_NAME_LENGTH = 12

# Colours in clockwise order. Index matches start square order.
COLOURS = ["red", "green", "yellow", "blue"]

# With 2 players the seats sit in opposite corners.
TWO_PLAYER_COLOURS = ["red", "yellow"]

# Track
TRACK_SQUARES = 52
START_SQUARES = {"red": 0, "green": 13, "yellow": 26, "blue": 39}
STAR_OFFSET = 8

# Safe squares: 4 start squares + 4 star squares (8 in total)
SAFE_SQUARES = set(START_SQUARES.values()) | {
    (s + STAR_OFFSET) % TRACK_SQUARES for s in START_SQUARES.values()
}  # {0, 8, 13, 21, 26, 34, 39, 47}

# Path of one piece (steps)
# step -1      : in start area
# step 0       : on own start square
# steps 1..50  : track squares
# steps 51..56 : home column
START_AREA_STEP = -1
LAST_TRACK_STEP = 50
FINAL_STEP = 56

# Dice and extra turns
DICE_MIN = 1
DICE_MAX = 6
SIX = 6
SIX_CANCEL_GROUP = 3  # every complete group of 3 consecutive sixes is cancelled

# CPU
CPU_DELAY_SECONDS = 0.5  # CPU must roll and move within 1 s (NFR 5.1.2)