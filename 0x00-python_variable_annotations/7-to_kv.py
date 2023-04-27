#!/usr/bin/env python3
""" Module for task 7
"""

from typing import Union, Tuple


def to_kv(k: str, v: Union[int, float]) -> Tuple[str, float]:
    """ Method to return sum of list of ints and floats
    """
    return (k, v * v)
