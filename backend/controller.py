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

    def quit(self):
        self.state = None
        self.seats = None
        self.phase = "idle"
        self.events = []
        return self.snapshot()

    def _start(self):
        self.state = GameState(self.seats)
        self.phase = "roll"
        self.extra_rolls = 0
        self.movable = []
        self.last_roll = None
        self.events = []
        self._say(f"{self.state.active().name}'s turn.")

    # ---------- player actions ----------

    def roll(self):
        self.events = []
        self._check(want_cpu=False, phase="roll")
        self._do_roll()
        return self.snapshot()

    def move(self, piece):
        self.events = []
        self._check(want_cpu=False, phase="move")
        self._play_move(piece)
        return self.snapshot()

    def cpu_step(self):
        """One CPU action: either a roll or a move."""
        self.events = []
        if self.state is None:
            raise GameError("No game in progress.")
        if self.state.finished:
            raise GameError("The game is over.")
        if not self.state.active().is_cpu:
            raise GameError("It is not the computer's turn.")
        if self.phase == "roll":
            self._do_roll()
        else:
            piece = cpu.choose_piece(self.state, self.state.dice_value, self.movable)
            self._play_move(piece)
        return self.snapshot()

    # ---------- turn flow ----------

    def _do_roll(self):
        s = self.state
        name = s.active().name
        value = dice.roll()
        self.last_roll = value
        s.dice_value = value

        if value == SIX:  # collect sixes, roll again (rule 14)
            s.rolls_collected.append(value)
            self._say(f"{name} rolled a 6 and rolls again.")
            return

        if len(s.rolls_collected) >= SIX_CANCEL_GROUP:
            self._say("Three sixes in a row are cancelled.")
        self._say(f"{name} rolled {value}.")
        s.pending_rolls = resolve_rolls(len(s.rolls_collected), value)
        s.rolls_collected = []
        self._advance()

    def _play_move(self, piece):
        s = self.state
        if piece not in range(len(s.active().pieces)):
            raise GameError("Invalid piece.")
        ok, reason = check_move(s, piece, s.dice_value)
        if not ok:
            raise GameError(reason)
        self._do_move(piece, s.dice_value)
        if not s.finished:
            self._advance()

    def _do_move(self, piece, roll):
        s = self.state
        name = s.active().name
        result = apply_move(s, piece, roll)

        for idx, _ in result["captured"]:
            self._say(f"{name} captured a piece of {s.players[idx].name}.")
        if result["won"]:
            s.finished = True
            s.winner = s.current
            s.pending_rolls = []
            self.movable = []
            self.phase = "over"
            self._say(f"{name} wins!")
        elif result["extra_roll"]:
            self.extra_rolls += 1  # taken after the current rolls (rule 13)

    def _advance(self):
        """Play pending rolls, then extra rolls, then pass the turn."""
        s = self.state
        self.movable = []
        while True:
            if s.pending_rolls:
                roll = s.pending_rolls.pop(0)
                s.dice_value = roll
                moves = valid_moves(s, roll)
                if not moves:
                    self._say(f"{s.active().name} has no possible move.")
                elif len(moves) == 1:
                    self._do_move(moves[0], roll)  # automatic single move
                    if s.finished:
                        return
                else:
                    self.movable = moves  # player or CPU must choose
                    self.phase = "move"
                    return
            elif self.extra_rolls > 0:
                self.extra_rolls -= 1
                self.phase = "roll"
                self._say(f"{s.active().name} rolls again.")
                return
            else:
                s.next_turn()
                self.phase = "roll"
                self._say(f"{s.active().name}'s turn.")
                return

    # ---------- helpers ----------

    def _check(self, want_cpu, phase):
        if self.state is None:
            raise GameError("No game in progress.")
        if self.state.finished:
            raise GameError("The game is over.")
        if self.state.active().is_cpu != want_cpu:
            raise GameError("It is the computer's turn.")
        if self.phase != phase:
            raise GameError("You have already rolled." if phase == "roll"
                            else "Roll the dice first.")

    def _say(self, text):
        self.events.append(text)
        if self.state:
            self.state.message = text

