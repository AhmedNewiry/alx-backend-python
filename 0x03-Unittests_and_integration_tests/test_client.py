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
    """Unit tests for GithubOrgClient class."""

    @parameterized.expand([
        ('google',),
        ('abc',),
    ])
    @patch('client.get_json')
    def test_org(self, org_name, mock_get_json):
        """Test that org property returns correct organization data.

        Verifies that GithubOrgClient.org calls get_json with the correct URL
        and returns the expected payload.
        """
        test_payload = {'login': org_name}
        mock_get_json.return_value = test_payload
        client = GithubOrgClient(org_name)
        result = client.org
        self.assertEqual(result, test_payload)
        mock_get_json.assert_called_once_with(f'https://api.github.com/orgs/{org_name}')

    def test_public_repos_url(self):
        """Test that _public_repos_url property returns correct URL.

        Verifies that _public_repos_url extracts the repos_url from the mocked org data.
        """
        test_payload = {'repos_url': 'https://api.github.com/orgs/test/repos'}
        with patch.object(GithubOrgClient, 'org', new_callable=PropertyMock) as mock_org:
            mock_org.return_value = test_payload
            client = GithubOrgClient('test')
            result = client._public_repos_url
            self.assertEqual(result, test_payload['repos_url'])

    @patch('client.get_json')
    @patch('client.GithubOrgClient._public_repos_url', new_callable=PropertyMock)
    def test_public_repos(self, mock_public_repos_url, mock_get_json):
        """Test that public_repos returns correct list of repositories.

        Verifies that public_repos fetches repos from _public_repos_url and
        extracts their names correctly.
        """
        test_url = 'https://api.github.com/orgs/test/repos'
        test_payload = [{'name': 'repo1'}, {'name': 'repo2'}]
        mock_public_repos_url.return_value = test_url
        mock_get_json.return_value = test_payload
        client = GithubOrgClient('test')
        result = client.public_repos()
        self.assertEqual(result, ['repo1', 'repo2'])
        mock_public_repos_url.assert_called_once()
        mock_get_json.assert_called_once_with(test_url)

    @parameterized.expand([
        ({'license': {'key': 'my_license'}}, 'my_license', True),
        ({'license': {'key': 'other_license'}}, 'my_license', False),
        ({'license': None}, 'my_license', False),
        ({}, 'my_license', False),
        (None, 'my_license', False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test that has_license identifies license presence correctly.

        Verifies that has_license returns True only if the repo's license key
        matches the provided license_key.
        """
        client = GithubOrgClient('test')
        result = client.has_license(repo, license_key)
        self.assertEqual(result, expected)


@parameterized_class([
    {
        'org_payload': org_payload,
        'repos_payload': repos_payload,
        'expected_repos': expected_repos,
        'apache2_repos': apache2_repos
    }
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests for GithubOrgClient class."""

    @classmethod
    def setUpClass(cls):
        """Set up class by mocking requests.get with fixture payloads."""
        cls.get_patcher = patch('requests.get', side_effect=cls.mocked_requests_get)
        cls.mock_get = cls.get_patcher.start()

    @classmethod
    def tearDownClass(cls):
        """Tear down class by stopping the requests.get patcher."""
        cls.get_patcher.stop()

    @staticmethod
    def mocked_requests_get(url):
        """Mock requests.get to return fixture payloads based on URL."""
        mock_response = Mock()
        if '/orgs/' in url:
            mock_response.json.return_value = TestIntegrationGithubOrgClient.org_payload
        elif '/repos' in url:
            mock_response.json.return_value = TestIntegrationGithubOrgClient.repos_payload
        else:
            print(f'Warning: Unexpected URL: {url}')
            mock_response.json.return_value = {}
        return mock_response

    def test_public_repos(self):
        """Test that public_repos returns expected repository list."""
        client = GithubOrgClient('google')
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        """Test that public_repos filters by license correctly."""
        client = GithubOrgClient('google')
        self.assertEqual(client.public_repos(license='apache-2.0'), self.apache2_repos)
