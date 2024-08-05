#!/usr/bin/env python3

"""
Measure runtime of the wait_n coroutin
"""
import time
import asyncio
import importlib
wait_n = importlib.import_module('1-concurrent_coroutines').wait_n


def measure_time(n: int, max_delay: int) -> float:
    """
    Measures the total execution time of the wait_n coroutine and returns
    the average time per coroutine execution.

    Args:
        n (int): The number of coroutines to run.
        max_delay (int): The maximum delay for each coroutine.

    Returns:
        float: The average time per coroutine in seconds.
    """
    start_time = time.time()
    asyncio.run(wait_n(n, max_delay))
    end_time = time.time()
    
    total_time = end_time - start_time
    average_time = total_time / n
    return average_time
