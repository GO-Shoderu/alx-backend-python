#!/usr/bin/env python3
"""Unit tests for the client module."""

import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized

from client import GithubOrgClient


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
        