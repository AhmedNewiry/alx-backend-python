#!/usr/bin/env python3
"""
Unit tests for the access_nested_map function from the utils module.
"""

import unittest
from parameterized import parameterized
from utils import access_nested_map  # Assuming utils is the module where the function is defined

class TestAccessNestedMap(unittest.TestCase):
    """
    Test case for the access_nested_map function.
    
    This class contains tests that verify the behavior of the
    access_nested_map function using various input scenarios.
    """

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        """
        Test that access_nested_map returns the expected value
        for given inputs.
        
        Args:
            nested_map (dict): The nested dictionary to access.
            path (tuple): The path of keys to follow in the
                          nested dictionary.
            expected: The expected value at the end of the path.
        """
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",)),
        ({"a": 1}, ("a", "b")),
    ])
    def test_access_nested_map_exception(self, nested_map, path):
        """
        Test that access_nested_map raises a KeyError with the expected
        message when the key is not found in the nested map.

        Args:
            nested_map (Mapping): The nested dictionary to access.
            path (Sequence): The path of keys to follow in the nested dictionary.
        """
        with self.assertRaises(KeyError) as context:
            access_nested_map(nested_map, path)

        # Check that the exception message is as expected
        self.assertEqual(str(context.exception), f"'{path[-1]}'")

if __name__ == "__main__":
    unittest.main()
