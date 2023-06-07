#!/usr/bin/env python3
""" Test module for utils.py
"""

import unittest
from unittest.mock import patch, Mock
from parameterized import parameterized
from typing import Dict, Tuple, Union
# Import methods to test
from utils import access_nested_map, get_json


class TestAccessNestedMap(unittest.TestCase):
    """ Testing utils.access_nested_map
    """
    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(
            self,
            nested_map: Dict,
            path: Tuple[str],
            expected: Union[Dict, int]
            ) -> None:
        """ Test output for utils.access_nested_map"""
        self.assertEqual(access_nested_map(nested_map, path), expected)
    
    @parameterized.expand([
        ({}, ("a",), KeyError, "'a'"),
        ({"a": 1}, ("a", "b"), KeyError, "'b'"),
    ])
    def test_access_nested_map_exception(
            self,
            nested_map: Dict,
            path: Tuple[str],
            exception: Exception,
            msg: str
            ) -> None:
        """ Test exception raised for access nested map """
        with self.assertRaises(exception) as err:
            access_nested_map(nested_map, path)
        self.assertEqual(str(err.exception), msg)


class TestGetJson(unittest.TestCase):
    """ Testing utils.get_json
    """
    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    def test_get_json(
            self,
            url: str,
            payload: Dict
            ) -> None:
        """ Test output for utils.get_json
        """
        attr = {"json.return_value": payload}
        with patch("requests.get", return_value=Mock(**attr)) as response:
            self.assertEqual(get_json(url), payload)
            response.assert_called_once_with(url)
