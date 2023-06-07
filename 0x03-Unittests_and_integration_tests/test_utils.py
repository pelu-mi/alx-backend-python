#!/usr/bin/env python3
""" Test module for utils.py
"""

import unittest
from unittest.mock import patch
from parameterized import parameterized
from typing import Dict, Tuple, Union
# Import methods to test
from utils import access_nested_map


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
        ({}, ("a",), "a"),
        ({"a": 1}, ("a", "b"), "b"),
    ])
    def test_access_nested_map_exception(
            self,
            nested_map: Dict,
            path: Tuple[str],
            msg: str
            ) -> None:
        """ Test exception raised for access nested map """
        with self.assertRaises(KeyError) as err:
            access_nested_map(nested_map, path)
        self.assertEqual(str(err.exception), msg)
