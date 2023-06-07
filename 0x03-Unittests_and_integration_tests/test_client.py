#!/usr/bin/env python3
""" Test module for client.py
"""

import unittest
from unittest.mock import patch, Mock, MagicMock, PropertyMock
from parameterized import parameterized, parameterized_class
from typing import Dict
from requests import HTTPError
# Import methods to test
from client import GithubOrgClient
from fixtures import TEST_PAYLOAD


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


@parameterized_class([
    {
        "org_payload": TEST_PAYLOAD[0][0],
        "repos_payload": TEST_PAYLOAD[0][1],
        "expected_repos": TEST_PAYLOAD[0][2],
        "apache2_repos": TEST_PAYLOAD[0][3],
    },
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """ Integration test for GithubOrgClient
    """
    @classmethod
    def setUpClass(cls) -> None:
        """ Set up class fixtures and parameters for testing
        """
        route_payload = {
            'https://api.github.com/orgs/google': cls.org_payload,
            'https://api.github.com/orgs/google/repos': cls.repos_payload,
        }

        def get_payload(url):
            """ Get payload from parameterized class
            """
            if url in route_payload:
                return Mock(**{'json.return_value': route_payload[url]})
            return HTTPError

        cls.get_patcher = patch("requests.get", side_effect=get_payload)
        cls.get_patcher.start()

    def test_public_repos(self) -> None:
        """ Test the public repos method
        """
        self.assertEqual(
            GithubOrgClient("google").public_repos(),
            self.expected_repos,
        )

    def test_public_repos_with_license(self) -> None:
        """ Test the public repos that have a license
        """
        self.assertEqual(
            GithubOrgClient("google").public_repos(license="apache-2.0"),
            self.apache2_repos,
        )

    @classmethod
    def tearDownClass(cls) -> None:
        """ Tear down class fixtures and parameters after testing
        """
        cls.get_patcher.stop()
