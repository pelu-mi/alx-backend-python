#!/usr/bin/env python3
""" Test module for client.py
"""

import unittest
from unittest.mock import patch, Mock, MagicMock, PropertyMock
from parameterized import parameterized
from typing import Dict
# Import methods to test
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """ Testing client.GithubOrgClient
    """
    @parameterized.expand([
        ("google", {"login": "google"}),
        ("abc", {"message": "Not Found"}),
    ])
    @patch("client.get_json")
    def test_org(self, org: str, res: Dict, mock_fn: MagicMock) -> None:
        """ Test that GithubOrgClient.org returns the right value
        """
        mock_fn.return_value = MagicMock(return_value=res)
        git_client_test = GithubOrgClient(org)
        self.assertEqual(git_client_test.org(), res)
        org_url = "https://api.github.com/orgs/{}".format(org)
        mock_fn.assert_called_once_with(org_url)

    def test_public_repos_url(self) -> None:
        """ Test that the result of _public_repos_url is the expected one
        """
        with patch(
                "client.GithubOrgClient.org",
                new_callable=PropertyMock) as mock_org:
            mock_org.return_value = {
                "repos_url": "https://api.github.com/orgs/google/repos",
            }
            self.assertEqual(
                    GithubOrgClient("google")._public_repos_url,
                    "https://api.github.com/orgs/google/repos")

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json: MagicMock) -> None:
        """ Test the result of GithubOrgClient.public_repos
        """
        test_payload = {
            "repos_url": "https://api.github.com/users/google/repos",
            "repos": [
                {
                    "id": 8566972,
                    "name": "kratu",
                    "private": False,
                    "owner": {
                        "login": "google",
                        "id": 1342004,
                    },
                    "language": "JavaScript",
                    "description": None,
                },
                {
                    "id": 7411424,
                    "name": "sirius",
                    "private": False,
                    "owner": {
                        "login": "google",
                        "id": 1342004,
                    },
                    "language": None,
                    "description": "sirius",
                },
            ]
        }
        mock_get_json.return_value = test_payload["repos"]
        with patch(
                "client.GithubOrgClient._public_repos_url",
                new_callable=PropertyMock) as mock_public_repos_url:
            mock_public_repos_url.return_value = test_payload['repos_url']
            self.assertEqual(
                    GithubOrgClient("google").public_repos(),
                    ["kratu", "sirius"])
            mock_public_repos_url.assert_called_once()
        mock_get_json.assert_called_once()

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo: Dict, key: str, expected: bool) -> None:
        """ Test GithubOrgClient.has_license
        """
        git_client_org = GithubOrgClient("google")
        git_client_has_license = git_client_org.has_license(repo, key)
        self.assertEqual(git_client_has_license, expected)
