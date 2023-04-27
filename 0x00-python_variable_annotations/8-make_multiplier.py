#!/usr/bin/env python3
""" Module for task 8
"""

from typing import Callable


def make_multiplier(multiplier: float) -> Callable[[float], float]:
    """ Method to return function that multiplies a number by multiplier
    """
    def multiply(n: float) -> float:
        """ Method returned by make_multiplier """
        return n * multiplier
    # Return the defined function
    return multiply
