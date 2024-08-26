#!/usr/bin/env python3
"""
Unit tests for the GithubOrgClient class from the client module.
"""

import unittest
from unittest.mock import patch
from parameterized import parameterized
from client import GithubOrgClient  # Assuming client is where GithubOrgClient is defined


class TestGithubOrgClient(unittest.TestCase):
    """
    Test case for the GithubOrgClient class.

    This class contains tests that verify the behavior of the org
    method using various organization examples.
    """

    @parameterized.expand([
        ("google", {"login": "google", "id": 1}),
        ("abc", {"login": "abc", "id": 2}),
    ])
    @patch('client.get_json')
    def test_org(self, org_name, expected_result, mock_get_json):
        """
        Test that GithubOrgClient.org returns the correct value and that
        get_json is called once with the correct URL.

        Args:
            org_name (str): The name of the organization to retrieve.
            expected_result (dict): The expected result from the org method.
            mock_get_json (Mock): The mock object for the get_json function.
        """
        mock_get_json.return_value = expected_result

        client = GithubOrgClient(org_name)
        result = client.org

        # Verify that get_json was called once with the correct URL
        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )

        # Verify that the result is as expected
        self.assertEqual(result, expected_result)


if __name__ == "__main__":
    unittest.main()
