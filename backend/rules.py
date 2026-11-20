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