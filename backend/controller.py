# controller.py
# Game Controller. Input: player actions. Output: updated state for the UI.

import dice
import cpu
from config import MIN_PLAYERS, MAX_PLAYERS, MAX_NAME_LENGTH, SIX, SIX_CANCEL_GROUP
from rules import check_move, valid_moves, apply_move, resolve_rolls
from state import GameState


class GameError(Exception):
    """A rejected action. The message is shown to the player."""