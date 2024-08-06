#!/usr/bin/env python3
"""
This module measures the runtime of
running async_comprehension in parallel.
"""
import asyncio
import time
from typing import List
from 1_async_comprehension import async_comprehension


async def measure_runtime() -> float:
    """
    Coroutine that measures the total runtime
    of running async_comprehension
    four times in parallel using asyncio.gather.
    Returns:
        float: The total runtime in seconds.
    """
    start_time = time.perf_counter()
    await asyncio.gather(*(async_comprehension() for _ in range(4)))
    total_runtime = time.perf_counter() - start_time
    return total_runtime
