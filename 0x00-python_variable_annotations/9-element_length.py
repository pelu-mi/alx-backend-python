#!/usr/bin/env python3
""" Module for task 9
"""

from typing import Iterable, Sequence, List, Tuple


def element_length(lst: Iterable[Sequence]) -> List[Tuple[Sequence, int]]:
    """ Function to compute length of a sequence
    """
    return [(i, len(i)) for i in lst]
