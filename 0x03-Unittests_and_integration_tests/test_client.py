#!/usr/bin/env python3
"""Unit tests for the client module."""

import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized, parameterized_class

from client import GithubOrgClient
from fixtures import TEST_PAYLOAD


class TestGithubOrgClient(unittest.TestCase):
    """Tests for GithubOrgClient."""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch("client.get_json")
    def test_org(self, org_name, mock_get_json):
        """Test that org property calls get_json and returns its result."""
        expected = {"org": org_name}
        mock_get_json.return_value = expected

        client = GithubOrgClient(org_name)
        result = client.org

        expected_url = "https://api.github.com/orgs/{}".format(org_name)
        mock_get_json.assert_called_once_with(expected_url)
        self.assertEqual(result, expected)

    def test_public_repos_url(self):
        """Test that _public_repos_url uses org['repos_url'] correctly."""
        payload = {"repos_url": "https://api.github.com/orgs/google/repos"}

        with patch(
            "client.GithubOrgClient.org",
            new_callable=PropertyMock,
            return_value=payload,
        ) as mock_org:
            client = GithubOrgClient("google")
            result = client._public_repos_url

        self.assertEqual(result, payload["repos_url"])
        mock_org.assert_called_once()

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        """Test that public_repos returns the expected list of repo names."""
        payload = [
            {"name": "repo1"},
            {"name": "repo2"},
            {"name": "repo3"},
        ]
        mock_get_json.return_value = payload

        with patch(
            "client.GithubOrgClient._public_repos_url",
            new_callable=PropertyMock,
            return_value="https://api.github.com/orgs/google/repos",
        ) as mock_repos_url:
            client = GithubOrgClient("google")
            repos = client.public_repos()

        self.assertEqual(repos, ["repo1", "repo2", "repo3"])
        mock_repos_url.assert_called_once()
        mock_get_json.assert_called_once_with(
            "https://api.github.com/orgs/google/repos",
        )

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test that has_license returns the correct boolean."""
        result = GithubOrgClient.has_license(repo, license_key)
        self.assertEqual(result, expected)


@parameterized_class(
    ("org_payload", "repos_payload", "expected_repos", "apache2_repos"),
    TEST_PAYLOAD,
)
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests for GithubOrgClient.public_repos."""

    @classmethod
    def setUpClass(cls):
        """Set up class fixtures and patch requests.get."""
        cls.get_patcher = patch("requests.get")
        mock_get = cls.get_patcher.start()

        def mocked_get(url):
            """Mocked requests.get that returns different payloads by URL."""
            class MockResponse:
                def __init__(self, json_data):
                    self._json_data = json_data

                def json(self):
                    return self._json_data

            # If the URL is the repos_url, return repos_payload
            if url == cls.org_payload["repos_url"]:
                return MockResponse(cls.repos_payload)

            # Otherwise, assume it's the org URL
            return MockResponse(cls.org_payload)

        mock_get.side_effect = mocked_get

    @classmethod
    def tearDownClass(cls):
        """Stop the requests.get patcher."""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Integration test: public_repos without license filter."""
        client = GithubOrgClient("google")
        result = client.public_repos()
        self.assertEqual(result, self.expected_repos)

    def test_public_repos_with_license(self):
        """Integration test: public_repos filtered by license."""
        client = GithubOrgClient("google")
        result = client.public_repos(license="apache-2.0")
        self.assertEqual(result, self.apache2_repos)
