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

class GameState:
    def __init__(self, seats: list):
        """seats: list of {"name": str, "is_cpu": bool}, 2 to 4 items."""
        colours = TWO_PLAYER_COLOURS if len(seats) == 2 else COLOURS
        self.players = [
            Player(name=s["name"], colour=colours[i], is_cpu=s["is_cpu"])
            for i, s in enumerate(seats)
        ]
        self.current = random.randrange(len(self.players))  # random first player
        self.pending_rolls = []   # rolls waiting to be played this turn
        self.rolls_collected = [] # sixes collected so far (rule 14)
        self.dice_value = None    # roll being played right now
        self.winner = None        # player index when game ends
        self.finished = False
        self.message = ""