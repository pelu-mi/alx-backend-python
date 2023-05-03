#!/usr/bin/env python3
""" Module for task 1
"""

import asyncio
from random import uniform
from typing import List
task_wait_random = __import__('3-tasks').task_wait_random


async def task_wait_n(n: int, max_delay: int) -> List[float]:
    """ Function to generate random delay using asyncio n times
    """
    arr: List[float] = []
    arr = await asyncio.gather(*(task_wait_random(max_delay) for i in range(n)))
    return sorted(arr)
