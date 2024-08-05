#!/usr/bin/env python3
"""
Module to create a coroutine that spawns multiple tasks
"""
import asyncio
from importlib import  import_module
task_wait_random = import_module('3-tasks').task_wait_random


def task_wait_n(n: int, max_delay: int):
    """
    Function that spawns n tasks with max_delay and gathers their results.
    The delays are returned in ascending order.

    Args:
    n (int): The number of tasks to create.
    max_delay (int): The maximum delay for each task.

    Returns:
    List[float]: A list of delays sorted in ascending order.
    """
    async def gather_delays():
        tasks = [task_wait_random(max_delay) for _ in range(n)]
        delays = [await task for task in asyncio.as_completed(tasks)]
        return sorted(delays)
    return asyncio.run(gather_delays())
