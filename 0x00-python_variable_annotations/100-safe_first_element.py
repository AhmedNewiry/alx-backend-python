#!/usr/bin/env python3
"""
This module contains a function `safe_first_element`
that retrieves the first element
from a sequence if it is not empty.
"""

from typing import Sequence, Any, Union


def safe_first_element(lst: Sequence[Any]) -> Union[Any, None]:
    """
    Return the first element of a sequence if it
    is not empty; otherwise, return None.

    Args:
    lst (Sequence[Any]): A sequence (e.g., list or tuple) from which
    to get the first element.

    Returns:
    Union[Any, None]: The first element of the sequence
    if it is not empty; otherwise, None.
    """
    if lst:
        return lst[0]
    else:
        return None
