#!/usr/bin/env python3
""" Module for task 0
"""

from typing import Union
import asyncio
from random import uniform


async def wait_random(max_delay: Union[int, float] = 10) -> float:
    """ Function to generate random delay using asyncio
    """
    delay: float = uniform(0, max_delay)
    await asyncio.sleep(delay)
    return delay
