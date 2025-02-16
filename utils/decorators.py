import functools
from typing import Callable

from performance_monitoring.memory import memory_object_report


def memory_profiler_func(func: Callable) -> Callable:
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        print(f"\n🔍 Analyzing memory for function: {func.__name__}")
        memory_object_report(result)
        return result

    return wrapper
