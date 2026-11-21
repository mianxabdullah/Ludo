# state.py
# Game State. Input: updates from the controller. Output: current state.

import random
from dataclasses import dataclass, field

from config import (
    COLOURS,
    TWO_PLAYER_COLOURS,
    PIECES_PER_PLAYER,
    START_AREA_STEP,
    FINAL_STEP,
)
