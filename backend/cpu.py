# cpu.py
# CPU Player. Input: Game State, dice value, valid moves. Output: chosen piece.

from config import START_AREA_STEP, FINAL_STEP, SAFE_SQUARES
from rules import square_of


def _new_step(step: int, roll: int) -> int:
    return 0 if step == START_AREA_STEP else step + roll

def _would_finish(state, piece: int, roll: int) -> bool:
    step = state.active().pieces[piece]
    return _new_step(step, roll) == FINAL_STEP

def _would_capture(state, piece: int, roll: int) -> bool:
    player = state.active()
    new_step = _new_step(player.pieces[piece], roll)
    square = square_of(player.colour, new_step)
    if square is None or square in SAFE_SQUARES:
        return False
    for other in state.players:
        if other is player:
            continue
        for s in other.pieces:
            if square_of(other.colour, s) == square:
                return True
    return False

def choose_piece(state, roll: int, moves: list) -> int:
    """Pick one piece index from 'moves' (must not be empty)."""
    pieces = state.active().pieces

    # 1. finish a piece
    for i in moves:
        if _would_finish(state, i, roll):
            return i
    # 2. capture an opponent
    for i in moves:
        if _would_capture(state, i, roll):
            return i
    # 3. bring a piece out of the start area
    for i in moves:
        if pieces[i] == START_AREA_STEP:
            return i
    # 4. move the piece that is furthest ahead
    return max(moves, key=lambda i: pieces[i])