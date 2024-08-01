#!/usr/bin/env python3
"""
This module provides a function to get the floor value of a float.

The floor function takes a float argument and returns its floor value as an integer.
"""

import math

def floor(n: float) -> int:
    """
    Return the floor value of a float.

    Args:
        n (float): The float number to floor.

    Returns:
        int: The floor value of the float.
    """
    return math.floor(n)
