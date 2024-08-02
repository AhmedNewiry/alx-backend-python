#!/usr/bin/env python3
"""
Module providing a function to zoom (duplicate) elements in a list.
"""

from typing import List, Tuple

def zoom_array(lst: Tupe,
               factor: int = 2) -> List:
    """
    Zoom (duplicate) elements in the list based on the given factor.

    Args:
        lst (List[Union[int, float]]): A list of integers
        or floats to be zoomed.
        factor (int, optional): The factor by which to
        duplicate the elements. Defaults to 2.

    Returns:
        List[Union[int, float]]: A list with each element
        duplicated `factor` times.
    """
    zoomed_in: List[Union[int, float]] = [
        item for item in lst
        for _ in range(factor)
    ]
    return zoomed_in

# Sample usage
array = [12, 72, 91]
zoom_2x = zoom_array(array)
zoom_3x = zoom_array(array, 30)
