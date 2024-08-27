#!/usr/bin/env python3
"""
Unit and integration tests for the GithubOrgClient class.
"""

import unittest
from typing import Dict
from unittest.mock import (
    MagicMock,
    Mock,
    PropertyMock,
    patch,
)
from parameterized import parameterized, parameterized_class
from requests import HTTPError

from client import (
    GithubOrgClient
)
from fixtures import TEST_PAYLOAD


class TestGithubOrgClient(unittest.TestCase):
    """Tests for the GithubOrgClient class."""

    @parameterized.expand([
        ("google", {"login": "google"}),
        ("abc", {"login": "abc"}),
    ])
    @patch("client.get_json")
    def test_org(self, org: str, expected_resp: Dict,
                 mock_get_json: MagicMock) -> None:
        """
        Tests that the `org` method of GithubOrgClient returns the correct
        response.

        Args:
            org (str): The name of the organization to test.
            expected_resp (Dict): The expected response from the `org` method.
            mock_get_json (MagicMock): Mocked get_json function.
        """
        mock_get_json.return_value = expected_resp
        gh_org_client = GithubOrgClient(org)

        # Test that the org method returns the expected response
        self.assertEqual(gh_org_client.org, expected_resp)

        # Verify that get_json was called once with the correct URL
        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org}"
        )

    def test_public_repos_url(self):
        """
        Test the _public_repos_url method.

        This method should return the correct URL based on the mocked org
        property.
        """
        with patch(
                'client.GithubOrgClient.org',
                new_callable=property
        ) as mock_org:
            mock_org.return_value = {
                "repos_url": "https://api.github.com/orgs/test/repos"
            }
            client = GithubOrgClient("test")

            # Test _public_repos_url method
            self.assertEqual(
                client._public_repos_url,
                "https://api.github.com/orgs/test/repos"
            )

    @parameterized.expand([
        ("google", {"repos_url": "https://api.github.com/orgs/google/repos"},
         [{"name": "repo1"}, {"name": "repo2"}]),
        ("abc", {"repos_url": "https://api.github.com/orgs/abc/repos"},
         [{"name": "repo3"}, {"name": "repo4"}])
    ])
    @patch("client.get_json")
    def test_public_repos(self, org: str, repos_url: Dict, 
                          repos_payload: List[Dict], 
                          mock_get_json: MagicMock) -> None:
        """
        Tests the `public_repos` method of GithubOrgClient.

        Args:
            org (str): The name of the organization to test.
            repos_url (Dict): The mocked URL returned by _public_repos_url.
            repos_payload (List[Dict]): The mocked list of repositories.
            mock_get_json (MagicMock): Mocked get_json function.
        """
        with patch("client.GithubOrgClient._public_repos_url", 
                   new_callable=MagicMock) as mock_public_repos_url:
            mock_public_repos_url.return_value = repos_url["repos_url"]
            mock_get_json.return_value = repos_payload

            gh_org_client = GithubOrgClient(org)
            
            # Test that the public_repos method returns the expected list
            self.assertEqual(gh_org_client.public_repos(), repos_payload)
            
            # Verify that _public_repos_url was called once
            mock_public_repos_url.assert_called_once()
            
            # Verify that get_json was called once with the correct URL
            mock_get_json.assert_called_once_with(repos_url["repos_url"])

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False)
    ])
    def test_has_license(self, repo, license_key, expected):
        """
        Test the has_license method.

        Args:
            repo (dict): The repository data to test.
            license_key (str): The license key to check for.
            expected (bool): The expected result.
        """
        client = GithubOrgClient("test")
        self.assertEqual(client.has_license(repo, license_key), expected)


class TestIntegrationGithubOrgClient(unittest.TestCase):
    """
    Integration tests for the GithubOrgClient class.
    """

    @classmethod
    def setUpClass(cls):
        """
        Set up the class by mocking requests.get.
        """
        cls.get_patcher = patch('requests.get')
        cls.mock_get = cls.get_patcher.start()

        cls.mock_get.side_effect = lambda url: type('Response', (), {
            'json': lambda: {
                'https://api.github.com/orgs/test': org_payload,
                'https://api.github.com/orgs/test/repos': repos_payload,
                'https://api.github.com/orgs/test/repos?license=apache-2.0':
                apache2_repos
            }[url]
        })()

    @classmethod
    def tearDownClass(cls):
        """
        Stop the patcher.
        """
        cls.get_patcher.stop()

    @parameterized_class([
        (org_payload, repos_payload, expected_repos, apache2_repos)
    ])
    def test_public_repos(self, org_payload, repos_payload, expected_repos,
                          apache2_repos):
        """
        Integration test for the public_repos method.

        Args:
            org_payload (dict): The payload for the organization.
            repos_payload (dict): The payload for the repositories.
            expected_repos (list): The expected list of repositories.
            apache2_repos (list): The expected list of repositories with
                                  Apache 2.0 license.
        """
        client = GithubOrgClient("test")
        self.assertEqual(client.public_repos(), expected_repos)

    def test_public_repos_with_license(self):
        """
        Integration test for public_repos method with license filter.
        """
        client = GithubOrgClient("test")
        self.assertEqual(
            client.public_repos(license="apache-2.0"),
            apache2_repos
        )
