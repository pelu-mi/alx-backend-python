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
    @patch('client.get_json')
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
        with patch("client.GithubOrgClient.org",
                new_callable=PropertyMock
                ) as mock_org:
            mock_org.return_value = {
                "repos_url": "https://api.github.com/orgs/google/repos",
            }
            self.assertEqual(GithubOrgClient("google")._public_repos_url,
                    "https://api.github.com/orgs/google/repos")
