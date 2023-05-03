#!/usr/bin/env python3
""" Module for task 0
"""

import asyncio
import time
async_comprehension = __import__('1-async_comprehension').async_comprehension


async def measure_runtime() -> float:
    """ Async method to find runtime
    """
    start = time.perf_counter()
    result = await asyncio.gather(async_comprehension(),
                                  async_comprehension(),
                                  async_comprehension(),
                                  async_comprehension())
    return time.perf_counter() - start
