#!/usr/bin/env python3
""" Module for task 10
"""

from typing import Sequence, Union, Any


# The types of the elements of the input are not known
def safe_first_element(lst: Sequence[Any]) -> Union[Any, None]:
    """ Return the first element if the list exists, else None
    """
    if lst:
        return lst[0]
    else:
        return None
