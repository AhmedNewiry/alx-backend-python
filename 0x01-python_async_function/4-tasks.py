#!/usr/bin/env python3
"""
Module to create a coroutine that spawns multiple tasks
"""
import asyncio
from importlib import import_module
from typing import List
task_wait_random = import_module('3-tasks').task_wait_random


async def task_wait_n(n: int, max_delay: int) -> List[float]:
    """
    Function that spawns n tasks with max_delay and gathers their results.
    The delays are returned in ascending order.

    Args:
    n (int): The number of tasks to create.
    max_delay (int): The maximum delay for each task.

    Returns:
    List[float]: A list of delays sorted in ascending order.
    """
    tasks = [task_wait_random(max_delay) for _ in range(n)]
    delays = await asyncio.gather(*tasks)

    sorted_delays = []
    while delays:
        min_delay = min(delays)
        sorted_delays.append(min_delay)
        delays.remove(min_delay)

    return sorted_delays
