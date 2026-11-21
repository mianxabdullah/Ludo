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

@dataclass
class Player:
    name: str
    colour: str
    is_cpu: bool
    # One step value per piece. -1 = start area, 0..56 = path, 56 = finished.
    pieces: list = field(default_factory=lambda: [START_AREA_STEP] * PIECES_PER_PLAYER)

    def progress(self) -> dict:
        """Pieces at start, on the board, finished (always sums to 4)."""
        at_start = sum(1 for p in self.pieces if p == START_AREA_STEP)
        finished = sum(1 for p in self.pieces if p == FINAL_STEP)
        return {
            "at_start": at_start,
            "on_board": len(self.pieces) - at_start - finished,
            "finished": finished,
        }
