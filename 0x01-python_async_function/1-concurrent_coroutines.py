#!/usr/bin/env python3
""" Module for task 1
"""

import asyncio
from random import uniform
from typing import List

wait_random = __import__('0-basic_async_syntax').wait_random


async def wait_n(n: int, max_delay: int) -> List[float]:
    """ Function to generate random delay using asyncio n times
    """
    arr: List[float] = []
    arr = await asyncio.gather(*(wait_random(max_delay) for i in range(n)))
    return sorted(arr)
