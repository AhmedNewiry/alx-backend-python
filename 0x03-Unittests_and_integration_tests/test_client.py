#!/usr/bin/env python3
"""
Unit and integration tests for the GithubOrgClient class.
"""

import unittest
from unittest.mock import patch
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
from fixtures import (org_payload, repos_payload, expected_repos,
                      apache2_repos)


class TestGithubOrgClient(unittest.TestCase):
    """
    Unit tests for the GithubOrgClient class methods.
    """

    @parameterized.expand([
        ("google",),
        ("abc",)
    ])
    @patch('client.get_json')
    def test_org(self, org_name, mock_get_json):
        """
        Test that GithubOrgClient.org returns the correct value.

        Args:
            org_name (str): The name of the organization to test.
            mock_get_json (MagicMock): Mocked get_json function.
        """
        mock_get_json.return_value = {"org": org_name}
        client = GithubOrgClient(org_name)

        # Test method
        self.assertEqual(client.org, {"org": org_name})
        mock_get_json.assert_called_once_with(
            f'https://api.github.com/orgs/{org_name}'
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

    @patch('client.get_json')
    @patch('client.GithubOrgClient._public_repos_url', new_callable=property)
    def test_public_repos(self, mock_public_repos_url, mock_get_json):
        """
        Test the public_repos method.

        Args:
            mock_public_repos_url (MagicMock): Mocked
            _public_repos_url property.
            mock_get_json (MagicMock): Mocked get_json function.
        """
        mock_public_repos_url.return_value = \
            "https://api.github.com/orgs/test/repos"
        mock_get_json.return_value = [
            {"name": "repo1"}, {"name": "repo2"}
        ]
        client = GithubOrgClient("test")

        # Test public_repos method
        self.assertEqual(
            client.public_repos(),
            [{"name": "repo1"}, {"name": "repo2"}]
        )
        mock_get_json.assert_called_once_with(
            "https://api.github.com/orgs/test/repos"
        )

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
