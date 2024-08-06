#!/usr/bin/env python3
"""
Module to create an asyncio Task from the wait_random coroutine.
"""
from importlib import import_module
import asyncio
wait_random = import_module('0-basic_async_syntax').wait_random


def task_wait_random(max_delay: int) -> asyncio.Task:
    """
    Creates an asyncio Task from the wait_random
    coroutine with the specified max_delay.
    Args:
        max_delay (int): The maximum delay for the wait_random coroutine.
    Returns:
        asyncio.Task: The asyncio Task object for the wait_random coroutine.
    """
    return asyncio.create_task(wait_random(max_delay))
