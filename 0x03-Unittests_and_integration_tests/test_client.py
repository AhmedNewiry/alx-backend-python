#!/usr/bin/env python3
"""Unit and integration tests for GithubOrgClient class."""

from typing import Dict, List, Union
import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
from fixtures import org_payload, repos_payload, expected_repos, apache2_repos
import requests
from utils import get_json


class TestGithubOrgClient(unittest.TestCase):
    """Test case for GithubOrgClient class functionality."""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch('utils.get_json')
    def test_org(self, org_name: str, mock_get_json: unittest.mock.MagicMock) -> None:
        """Test that GithubOrgClient.org returns the correct organization payload.

        Args:
            org_name: Name of the organization to test.
            mock_get_json: Mocked get_json function from utils module.
        """
        expected: Dict[str, str] = {"login": org_name}
        mock_get_json.return_value = expected
        client: GithubOrgClient = GithubOrgClient(org_name)
        result: Dict[str, str] = client.org
        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )
        self.assertEqual(result, expected)

    def test_public_repos_url(self) -> None:
        """Test that GithubOrgClient._public_repos_url returns correct URL.

        Verifies the property returns repos_url from mocked org payload.
        """
        with patch('client.GithubOrgClient.org',
                   new_callable=PropertyMock) as mock_org:
            mock_org.return_value = {
                "repos_url": "https://api.github.com/orgs/test/repos"
            }
            client: GithubOrgClient = GithubOrgClient("test")
            result: str = client._public_repos_url
            self.assertEqual(result, "https://api.github.com/orgs/test/repos")

    @patch('utils.get_json')
    def test_public_repos(self, mock_get_json: unittest.mock.MagicMock) -> None:
        """Test that GithubOrgClient.public_repos returns correct repo list.

        Args:
            mock_get_json: Mocked get_json function from utils module.
        """
        test_payload: List[Dict[str, str]] = [
            {"name": "repo1"},
            {"name": "repo2"}
        ]
        mock_get_json.return_value = test_payload
        with patch('client.GithubOrgClient._public_repos_url',
                   new_callable=PropertyMock) as mock_url:
            mock_url.return_value = "https://api.github.com/orgs/test/repos"
            client: GithubOrgClient = GithubOrgClient("test")
            result: List[str] = client.public_repos()
            self.assertEqual(result, ["repo1", "repo2"])
            mock_url.assert_called_once()
            mock_get_json.assert_called_once_with(
                "https://api.github.com/orgs/test/repos"
            )

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo: Dict[str, Dict[str, str]],
                        license_key: str, expected: bool) -> None:
        """Test that GithubOrgClient.has_license checks license correctly.

        Args:
            repo: Repository dictionary with license information.
            license_key: License key to check against.
            expected: Expected boolean result.
        """
        client: GithubOrgClient = GithubOrgClient("test")
        result: bool = client.has_license(repo, license_key)
        self.assertEqual(result, expected)


@parameterized_class([
    {
        "org_payload": org_payload,
        "repos_payload": repos_payload,
        "expected_repos": expected_repos,
        "apache2_repos": apache2_repos
    }
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration test case for GithubOrgClient with fixture-based payloads."""

    @classmethod
    def setUpClass(cls) -> None:
        """Set up class by mocking requests.get with fixture payloads."""
        cls.get_patcher = patch('requests.get')
        cls.mock_get = cls.get_patcher.start()

        def side_effect(url: str) -> unittest.mock.MagicMock:
            """Side effect for mocked requests.get to return fixture payloads.

            Args:
                url: URL being requested.

            Returns:
                Mock response object with appropriate JSON payload.
            """
            class MockResponse:
                def __init__(self, json_data: Union[Dict, List, None]):
                    self.json_data = json_data

                def json(self) -> Union[Dict, List, None]:
                    """Return the JSON payload."""
                    return self.json_data

            if url == "https://api.github.com/orgs/test":
                return MockResponse(cls.org_payload)
            if url == cls.org_payload.get("repos_url"):
                return MockResponse(cls.repos_payload)
            return MockResponse(None)

        cls.mock_get.side_effect = side_effect

    @classmethod
    def tearDownClass(cls) -> None:
        """Tear down class by stopping the requests.get patcher."""
        cls.get_patcher.stop()

    def test_public_repos(self) -> None:
        """Test that public_repos returns expected repos from fixtures."""
        client: GithubOrgClient = GithubOrgClient("test")
        result: List[str] = client.public_repos()
        self.assertEqual(result, self.expected_repos)

    def test_public_repos_with_license(self) -> None:
        """Test that public_repos with apache-2.0 license filter works."""
        client: GithubOrgClient = GithubOrgClient("test")
        result: List[str] = client.public_repos(license="apache-2.0")
        self.assertEqual(result, self.apache2_repos)


if __name__ == '__main__':
    unittest.main()
