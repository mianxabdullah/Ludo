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

    def new_game(self, mode, players, humans, names):
        if not MIN_PLAYERS <= players <= MAX_PLAYERS:
            raise GameError("Choose 2, 3 or 4 players.")
        if mode == "single":
            humans = 1
        elif mode == "multi":
            if not 2 <= humans <= players:
                raise GameError(f"Choose 2 to {players} human players.")
        else:
            raise GameError("Unknown mode.")

        chosen = []
        for i in range(humans):
            name = names[i].strip() if i < len(names) else ""
            if not name:
                name = f"Player {i + 1}"
            if len(name) > MAX_NAME_LENGTH:
                raise GameError(f"A name can have at most {MAX_NAME_LENGTH} characters.")
            chosen.append(name)
        if len({n.lower() for n in chosen}) < len(chosen):
            raise GameError("Each player needs a different name.")

        self.seats = [{"name": n, "is_cpu": False} for n in chosen]
        self.seats += [{"name": f"CPU {i + 1}", "is_cpu": True}
                       for i in range(players - humans)]
        self._start()
        return self.snapshot()

    def restart(self):
        if not self.seats:
            raise GameError("No game to restart.")
        self._start()
        return self.snapshot()

