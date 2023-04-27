#!/usr/bin/env python3
""" Module for task 9
"""

from typing import Mapping, Union, Any, TypeVar


T = TypeVar('T')


def safely_get_value(dct: Mapping, key: Any,
                     default: Union[T, None] = None) -> Union[Any, T]:
    """ Function to safely get value from dict
    """
    if key in dct:
        return dct[key]
    else:
        return default
