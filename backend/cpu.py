# cpu.py
# CPU Player. Input: Game State, dice value, valid moves. Output: chosen piece.

from config import START_AREA_STEP, FINAL_STEP, SAFE_SQUARES
from rules import square_of


def _new_step(step: int, roll: int) -> int:
    return 0 if step == START_AREA_STEP else step + roll