#!/usr/bin/env python3
"""
This module defines a function sum_list which takes a list of floats
as an argument and returns their sum as a float.
"""

from typing import List

def sum_list(input_list: List[float]) -> float:
    """
    Returns the sum of a list of floats.

    Args:
        input_list (List[float]): A list of float numbers.

    Returns:
        float: The sum of the float numbers in the list.
    """
    return sum(input_list)
