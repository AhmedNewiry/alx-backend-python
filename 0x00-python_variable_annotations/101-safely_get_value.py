#!/usr/bin/env python3

"""
Module for safely retrieving values from
a dictionary with a default fallback
"""

from typing import Mapping, TypeVar, Any, Union

# Define a TypeVar to represent the type of the default value
T = TypeVar('T')


def def safely_get_value(
                         dct: Mapping,
                         key: Any,
                         default: Union[T, None] = None
                         ) -> Union[Any, T]:
    """
    Safely get a value from a dictionary given a key.
    If the key is not present, return the default value.

    Args:
    dct (Mapping[Any, Any]): A mapping (e.g., dictionary) from
    which to get the value.
    key (Any): The key whose associated value is to be returned.
    default (Union[T, None], optional): The value to return if
    the key is not found in the dictionary. Defaults to None.

    Returns:
    Union[Any, T]: The value associated with the key if present;
    otherwise, the default value.
    """
    if key in dct:
        return dct[key]
    else:
        return default
