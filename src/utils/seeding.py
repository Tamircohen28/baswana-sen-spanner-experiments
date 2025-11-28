"""Random seeding utilities for reproducibility."""

import random
import numpy as np


def set_seed(seed: int) -> None:
    """
    Set random seed for both Python's random module and numpy.
    
    Args:
        seed: Integer seed value
    """
    random.seed(seed)
    np.random.seed(seed)

