#!/usr/bin/env python3
""" Module for task 12
"""

from typing import List, Tuple


def zoom_array(lst: Tuple, factor: int = 2) -> List:
    """ Function to zoom array
    """
    zoomed_in: List = [
        item for item in lst
        for i in range(factor)
    ]
    return zoomed_in


array: List = [12, 72, 91]

zoom_2x: List = zoom_array(tuple(array))

zoom_3x: List = zoom_array(tuple(array), 3)
