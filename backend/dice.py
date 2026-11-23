# dice.py
# Dice Module. Input: roll request. Output: integer 1 to 6.

import random

from config import DICE_MIN, DICE_MAX

# SystemRandom uses OS randomness, so the next value cannot be predicted.
_rng = random.SystemRandom()


def roll() -> int:
    """Return one fair dice value from DICE_MIN to DICE_MAX."""
    return _rng.randint(DICE_MIN, DICE_MAX)

