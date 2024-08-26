#!/usr/bin/env python3
"""Unit tests for the GithubOrgClient class from the client module.
"""

import unittest
from typing import Dict
from unittest.mock import (
    MagicMock,
    PropertyMock,
    patch,
)
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
from fixtures import TEST_PAYLOAD


class TestGithubOrgClient(unittest.TestCase):
    """Test case for the GithubOrgClient class.

    This class contains tests that verify the behavior of the org method
    using various organization examples.
    """

    @parameterized.expand([
        ("google", {"login": "google"}),
        ("abc", {"login": "abc"}),
    ])
    @patch("client.get_json")
    def test_org(
        self, org_name: str, expected_result: Dict, mock_get_json: MagicMock
    ) -> None:
        """Test that GithubOrgClient.org returns the correct value and that
        get_json is called once with the correct URL.

        Args:
            org_name (str): The name of the organization to retrieve.
            expected_result (dict): The expected result from the org method.
            mock_get_json (MagicMock): The mock object for the get_json
                                       function.
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

    def test_public_repos_url(self) -> None:
        """Test that GithubOrgClient._public_repos_url returns the expected
        URL based on the org property.

        Use patch as a context manager to mock the org property and ensure
        that _public_repos_url returns the correct URL.
        """
        with patch(
            "client.GithubOrgClient.org", new_callable=PropertyMock
        ) as mock_org:
            # Set the return value for the mocked org property
            mock_org.return_value = {
                "repos_url": "https://api.github.com/orgs/google/repos"
            }

            client = GithubOrgClient("google")
            result = client._public_repos_url

            # Verify that the result is as expected
            expected_url = "https://api.github.com/orgs/google/repos"
            self.assertEqual(result, expected_url)

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json: MagicMock) -> None:
        """Tests the public_repos method."""
        test_payload = {
            'repos_url': "https://api.github.com/orgs/google/repos",
            'repos': [
                {
                    "id": 7697149,
                    "name": "episodes.dart",
                    "private": False,
                    "owner": {
                        "login": "google",
                        "id": 1342004,
                    },
                    "fork": False,
                    "url": "https://api.github.com/repos/google/episodes.dart",
                    "created_at": "2013-01-19T00:31:37Z",
                    "updated_at": "2019-09-23T11:53:58Z",
                    "has_issues": True,
                    "forks": 22,
                    "default_branch": "master",
                },
                {
                    "id": 8566972,
                    "name": "kratu",
                    "private": False,
                    "owner": {
                        "login": "google",
                        "id": 1342004,
                    },
                    "fork": False,
                    "url": "https://api.github.com/repos/google/kratu",
                    "created_at": "2013-03-04T22:52:33Z",
                    "updated_at": "2019-11-15T22:22:16Z",
                    "has_issues": True,
                    "forks": 32,
                    "default_branch": "master",
                },
            ]
        }
        mock_get_json.return_value = test_payload['repos']
        with patch(
            "client.GithubOrgClient._public_repos_url",
            new_callable=PropertyMock
        ) as mock_public_repos_url:
            mock_public_repos_url.return_value = test_payload['repos_url']

            client = GithubOrgClient("google")
            result = client.public_repos()

            # Verify that the result is as expected
            expected_repos = ["episodes.dart", "kratu"]
            self.assertEqual(result, expected_repos)

            mock_public_repos_url.assert_called_once()
        mock_get_json.assert_called_once()

    @parameterized.expand([
        ({"license": {"key": "bsd-3-clause"}}, "bsd-3-clause", True),
        ({"license": {"key": "bsl-1.0"}}, "bsd-3-clause", False),
    ])
    def test_has_license(
        self, repo: Dict, license_key: str, expected_result: bool
    ) -> None:
        """Test that GithubOrgClient.has_license correctly identifies the
        presence of a license in a repository.

        Args:
            repo (dict): The repository data to check for a license.
            license_key (str): The license key to look for.
            expected_result (bool): The expected result of the license check.
        """
        client = GithubOrgClient("google")
        result = client.has_license(repo, license_key)

        # Verify that the result is as expected
        self.assertEqual(result, expected_result)


@parameterized_class([
    {
        'org_payload': TEST_PAYLOAD[0][0],
        'repos_payload': TEST_PAYLOAD[0][1],
        'expected_repos': TEST_PAYLOAD[0][2],
        'apache2_repos': TEST_PAYLOAD[0][3],
    },
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests for the GithubOrgClient class."""

    @classmethod
    def setUpClass(cls) -> None:
        """Set up the class before any tests are run."""
        route_payload = {
            'https://api.github.com/orgs/google': cls.org_payload,
            'https://api.github.com/orgs/google/repos': cls.repos_payload,
        }

        def get_payload(url):
            if url in route_payload:
                return MagicMock(**{'json.return_value': route_payload[url]})
            return HTTPError

        cls.get_patcher = patch("requests.get", side_effect=get_payload)
        cls.get_patcher.start()

    def test_public_repos(self) -> None:
        """Test the public_repos method."""
        self.assertEqual(
            GithubOrgClient("google").public_repos(), self.expected_repos
        )

    def test_public_repos_with_license(self) -> None:
        """Test the public_repos method with a license."""
        self.assertEqual(
            GithubOrgClient("google").public_repos(license="apache-2.0"),
            self.apache2_repos,
        )

    @classmethod
    def tearDownClass(cls) -> None:
        """Clean up after the tests are run."""
        cls.get_patcher.stop()


if __name__ == "__main__":
    unittest.main()
