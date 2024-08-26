#!/usr/bin/env python3
"""
Unit tests for the access_nested_map function from the utils module.
"""

import unittest
from unittest.mock import patch, Mock, MagickMock
from parameterized import parameterized
from utils import access_nested_map, get_json, memoize


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
            path (Sequence): The path of keys to
            follow in the nested dictionary.
        """
        with self.assertRaises(KeyError) as context:
            access_nested_map(nested_map, path)

        # Check that the exception message is as expected
        self.assertEqual(str(context.exception), f"'{path[-1]}'")


class TestGetJson(unittest.TestCase):
    """unit tests for the get_json function"""

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    def test_get_json(self, test_url, test_payload):
        """checks if it returns the expected result"""
        with patch('utils.requests.get') as mock_get:
            mock_response = Mock()
            mock_response.json.return_value = test_payload
            mock_get.return_value = mock_response

            result = get_json(test_url)

            mock_get.assert_called_once_with(test_url)
            self.assertEqual(result, test_payload)


class TestMemoize(unittest.TestCase):
    """unit test for the memoize decorator."""
    def test_memoize(self):
        """ensure the memoize decorator cahes the result"""
        class TestClass:
            """Class to demonstrate memoization."""
            def a_method(self):
                """Simple method that returns 42."""
                return 42

            @memoize
            def a_property(self):
                """Simple method that returns 42."""
                return self.a_method()

        with patch.object(
                TestClass, 'a_method', return_value=42
                ) as mock_method:
            test_obj = TestClass()

            self.assertEqual(test_obj.a_property, 42)
            mock_method.assert_called_once()

            self.assertEqual(test_obj.a_property, 42)
            mock_method.assert_called_once()


if __name__ == "__main__":
    unittest.main()
