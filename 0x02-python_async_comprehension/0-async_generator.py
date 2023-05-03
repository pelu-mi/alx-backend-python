#!/usr/bin/env python3
""" Module for task 0
"""

import asyncio
from random import uniform
from typing import Generator


async def async_generator() -> Generator[int, None, None]:
    """ Async Generator method
    """
    for i in range(10):
        await asyncio.sleep(1)
        yield uniform(0, 10)
