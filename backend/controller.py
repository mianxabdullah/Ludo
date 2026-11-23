# controller.py
# Game Controller. Input: player actions. Output: updated state for the UI.

import dice
import cpu
from config import MIN_PLAYERS, MAX_PLAYERS, MAX_NAME_LENGTH, SIX, SIX_CANCEL_GROUP
from rules import check_move, valid_moves, apply_move, resolve_rolls
from state import GameState


class GameError(Exception):
    """A rejected action. The message is shown to the player."""

class Controller:
    def __init__(self):
        self.state = None
        self.seats = None
        self.phase = "idle"   # idle, roll, move, over
        self.extra_rolls = 0  # extra rolls from captures / finished pieces
        self.movable = []     # pieces the player may choose from
        self.last_roll = None
        self.events = []      # messages produced by the last action