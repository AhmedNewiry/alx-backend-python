#!/usr/bin/env python3
"""
This module defines a function to_kv which take
s a string k and an int or float v
as arguments and returns a tuple.
"""

from typing import Union, Tuple


def to_kv(k: str, v: Union[int, float]) -> Tuple[str, float]:
    """
    Returns a tuple where the first element is a string
    and the second element is the square of the number.

    Args:
        k (str): The string element of the tuple.
        v : The numeric value to be squared and used as the second element.

    Returns:
        Tuple[str, float]: A tuple with a string and the square of the number.
    """
    return (k, float(v ** 2))
