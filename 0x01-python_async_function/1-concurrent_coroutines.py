#!/usr/bin/env python3
"""
This module contains an asynchronous coroutine
that spawns multiple wait_random coroutines
and returns the list of all delays in ascending order.
"""
from typing import List
import asyncio
from 0-basic_async_syntax import wait_random


async def wait_n(n: int, max_delay: int) -> List[float]:
    """
    Spawns wait_random n times with the specified
    max_delay and returns the list of all the delays
    (float values) in ascending order.
    Args:
        n (int): Number of times to spawn wait_random.
        max_delay (int): Maximum delay in seconds.
    Returns:
        List[float]: List of delays in ascending order.
    """
    delays = await asyncio.gather(*(wait_random(max_delay) for _ in range(n)))
    sorted_delays = []
    while delays:
        min_delay = min(delays)
        sorted_delays.append(min_delay)
        delays.remove(min_delay)
    return sorted_delays
