# dice.py
# Dice Module. Input: roll request. Output: integer 1 to 6.

import random

from config import DICE_MIN, DICE_MAX

# SystemRandom uses OS randomness, so the next value cannot be predicted.
_rng = random.SystemRandom()


