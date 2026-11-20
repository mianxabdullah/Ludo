# rules.py
# Rules Engine. Input: Game State, dice value, chosen piece.
# Output: valid moves, move result, reason for an invalid move.

from config import (
    TRACK_SQUARES,
    START_SQUARES,
    SAFE_SQUARES,
    START_AREA_STEP,
    LAST_TRACK_STEP,
    FINAL_STEP,
    SIX,
    SIX_CANCEL_GROUP,
)


def square_of(colour: str, step: int):
    """Track square (0..51) of a piece, or None if it is not on the track."""
    if step < 0 or step > LAST_TRACK_STEP:
        return None  # in start area or in home column
    return (START_SQUARES[colour] + step) % TRACK_SQUARES


def check_move(state, piece: int, roll: int):
    """Return (True, "") if the move is valid, else (False, reason)."""
    step = state.active().pieces[piece]

    if step == FINAL_STEP:
        return False, "This piece has already finished."
    if step == START_AREA_STEP:
        if roll != SIX:
            return False, "You need a six to leave the start."
        return True, ""
    if step + roll > FINAL_STEP:
        return False, "You need the exact number to finish."
    return True, ""


def valid_moves(state, roll: int) -> list:
    """Indices of the active player's pieces that can move with this roll."""
    return [
        i for i in range(len(state.active().pieces))
        if check_move(state, i, roll)[0]
    ]


def apply_move(state, piece: int, roll: int) -> dict:
    """
    Make a move that was already checked.
    Returns {"captured": [(player_index, piece_index), ...],
             "finished_piece": bool, "won": bool, "extra_roll": bool}
    Extra roll here means capture or finished piece (rule 13).
    Sixes are handled by resolve_rolls.
    """
    player = state.active()
    step = player.pieces[piece]

    # Leave start with a six, otherwise advance by the roll.
    player.pieces[piece] = 0 if step == START_AREA_STEP else step + roll
    new_step = player.pieces[piece]

    captured = []
    square = square_of(player.colour, new_step)
    if square is not None and square not in SAFE_SQUARES:
        for idx, other in enumerate(state.players):
            if other is player:
                continue
            for j, other_step in enumerate(other.pieces):
                if square_of(other.colour, other_step) == square:
                    other.pieces[j] = START_AREA_STEP
                    captured.append((idx, j))

    finished_piece = new_step == FINAL_STEP
    won = all(s == FINAL_STEP for s in player.pieces)

    return {
        "captured": captured,
        "finished_piece": finished_piece,
        "won": won,
        "extra_roll": bool(captured) or finished_piece,
    }


def resolve_rolls(sixes: int, last: int) -> list:
    """
    Rule 14. 'sixes' = sixes rolled in a row, 'last' = the non-six that ended them.
    Every complete group of 3 sixes is cancelled; the rest are played, then 'last'.
    6,6,6,4 -> [4]    6x6,5 -> [5]    6,6,6,6,3 -> [6, 3]
    """
    leftover = sixes % SIX_CANCEL_GROUP
    return [SIX] * leftover + [last]