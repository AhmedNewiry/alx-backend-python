#!/usr/bin/env python3
"""
This module defines a function sum_mixed_list which takes a list of integers
and floats as an argument and returns their sum as a float.
"""
from typing import List, Union


def sum_mixed_list(mxd_lst: List[Union[int, float]]) -> float:
    """
    Returns the sum of a list containing integers and floats.

    Args:
        mxd_lst (List[Union[int, float]]): A list of integers and float numbers.

    Returns:
        float: The sum of the numbers in the list.
    """
    return float(sum(mxd_lst))
