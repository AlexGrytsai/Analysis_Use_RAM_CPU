import functools
import time
from typing import Callable


def timer_of_execution(func: Callable) -> Callable:
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()

        print(
            f"🕐 Execution time for '{func.__name__}': "
            f"{end_time - start_time:.4f} seconds"
        )
        return result

    return wrapper
