#!/usr/bin/env python3
"""
Unit and integration tests for the GithubOrgClient class.
"""

import unittest
from unittest.mock import patch, PropertyMock, Mock
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
from fixtures import org_payload, repos_payload, expected_repos, apache2_repos


class TestGithubOrgClient(unittest.TestCase):
    """
    Unit tests for the GithubOrgClient class.

    These tests cover:
    - org: Verifies that the org method returns the expected organization data.
    - _public_repos_url: Ensures the _public_repos_url
    property returns the correct URL.
    - public_repos: Checks that public_repos returns the expected
    list of repositories.
    - has_license: Tests that has_license correctly identifies
    the presence of a specified license.
    """

    @parameterized.expand([
        ("google",),
        ("abc",)
    ])
    @patch('client.get_json')
    def test_org(self, org_name, mock_get_json):
        """
        Test that the org method returns the correct organization data.

        Verifies that the `org` property of GithubOrgClient calls `get_json`
        with the correct URL and returns the expected organization data.
        """
        expected_json = {"login": org_name}
        mock_get_json.return_value = expected_json

        client = GithubOrgClient(org_name)
        org_data = client.org

        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )
        self.assertEqual(org_data, expected_json)

    @patch('client.GithubOrgClient.org', new_callable=PropertyMock)
    def test_public_repos_url(self, mock_org):
        """
        Test that the _public_repos_url property returns the correct URL.

        Ensures that the `_public_repos_url` property returns the URL for
        public repositories based on the organization
        data mocked by `mock_org`.
        """
        test_payload = {
            "repos_url": "https://api.github.com/orgs/test_org/repos"
        }
        mock_org.return_value = test_payload

        client = GithubOrgClient("test_org")
        public_repos_url = client._public_repos_url

        self.assertEqual(public_repos_url, test_payload["repos_url"])

    @patch('client.get_json')
    @patch(
        'client.GithubOrgClient._public_repos_url',
        new_callable=PropertyMock)
    def test_public_repos(self, mock_public_repos_url, mock_get_json):
        """
        Test that the public_repos method returns the
        correct list of repositories.

        Verifies that the `public_repos` method retrieves
        the list of repositories
        from the URL provided by `_public_repos_url`
        and matches the expected list.
        """
        test_url = "https://api.github.com/orgs/test_org/repos"
        test_payload = [
            {"name": "repo1"},
            {"name": "repo2"},
            {"name": "repo3"}
        ]
        expected_repos = ["repo1", "repo2", "repo3"]

        mock_public_repos_url.return_value = test_url
        mock_get_json.return_value = test_payload

        client = GithubOrgClient("test_org")
        repos = client.public_repos()

        self.assertEqual(repos, expected_repos)
        mock_public_repos_url.assert_called_once()
        mock_get_json.assert_called_once_with(test_url)

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
        ({"license": None}, "my_license", False),
        ({}, "my_license", False)
    ])
    def test_has_license(self, repo, license_key, expected_result):
        """
        Test that has_license returns the correct boolean value.

        Ensures that the `has_license` method correctly identifies whether the
        provided `repo` contains the specified `license_key` and matches
        the expected boolean result.
        """
        client = GithubOrgClient("test_org")
        result = client.has_license(repo, license_key)
        self.assertEqual(result, expected_result)


@parameterized_class([
    {"org_payload": org_payload,
     "repos_payload": repos_payload,
     "expected_repos": expected_repos,
     "apache2_repos": apache2_repos}
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """
    Integration tests for the GithubOrgClient class.

    These tests cover:
    - public_repos: Ensures that the public_repos method returns
    the expected list of repositories.
    - public_repos with license filter: Checks that public_repos
    correctly filters repositories by license.
    """

    @classmethod
    def setUpClass(cls):
        """
        Set up the class by patching `requests.get` with a mocked function
        that returns specific payloads.

        This setup allows testing without making actual HTTP requests.
        """
        cls.get_patcher = patch(
            'requests.get', side_effect=cls.mocked_requests_get
        )
        cls.get_patcher.start()

    @classmethod
    def tearDownClass(cls):
        """
        Tear down the class by stopping the patcher
        for `requests.get`.
        """
        cls.get_patcher.stop()

    @staticmethod
    def mocked_requests_get(url):
        """
        Mocked requests.get function to return specific
        payloads based on the URL.

        Provides mocked responses for different URLs to
        simulate API responses during testing.
        """
        mock_response = Mock()
        if 'orgs' in url:
            mock_response.json.return_value = (
                    TestIntegrationGithubOrgClient.org_payload
            )
        elif 'repos' in url:
            mock_response.json.return_value = (
                    TestIntegrationGithubOrgClient.repos_payload
            )
        return mock_response

    def test_public_repos(self):
        """
        Test the public_repos method to ensure it returns
        the expected list of repositories.

        This integration test verifies that the `public_repos`
        method of the GithubOrgClient class returns
        the repositories as expected based on the mocked responses.
        """
        client = GithubOrgClient('google')
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        """
        Test the public_repos method with a license filter.

        Verifies that the `public_repos` method correctly
        filters repositories based on the provided
        license and returns the expected list of repositories
        with the specified license.
        """
        client = GithubOrgClient('google')
        self.assertEqual(
            client.public_repos(license="apache-2.0"), self.apache2_repos
        )
