"""Timing utilities for performance measurement."""

import time
from contextlib import contextmanager
from functools import wraps
from typing import Callable, Any


@contextmanager
def Timer():
    """
    Context manager for measuring execution time.
    
    Usage:
        with Timer() as timer:
            # code to time
        elapsed = timer.elapsed
    
    Yields:
        Timer object with elapsed attribute
    """
    start = time.time()
    timer = type('Timer', (), {'elapsed': None})()
    try:
        yield timer
    finally:
        timer.elapsed = time.time() - start


def timed(func: Callable) -> Callable:
    """
    Decorator that measures execution time of a function.
    
    The function's return value is augmented with an 'elapsed_time' attribute.
    
    Usage:
        @timed
        def my_function():
            ...
        
        result = my_function()
        print(f"Took {result.elapsed_time} seconds")
    
    Args:
        func: Function to time
        
    Returns:
        Wrapped function with elapsed_time attribute
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        result.elapsed_time = time.time() - start
        return result
    return wrapper

