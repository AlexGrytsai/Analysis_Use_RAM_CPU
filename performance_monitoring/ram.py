import psutil
import time
import functools
from typing import Callable
import threading


def print_ram_usage(
    mem_usage: list, interval: float, func_name: str, is_detail: bool
) -> None:
    print(f"📊 Using RAM in the process of performing a '{func_name}':")
    if is_detail:
        for i, usage in enumerate(mem_usage):
            print(f"  Time {i * interval:.2f} seconds: {usage:.2f} MB")

    max_mem = max(mem_usage) if mem_usage else 0
    print(f"\n  📊 Peak use RAM: {max_mem:.2f} MB")


def ram_monitor_decorator(
    interval: float = 0.1,
    is_detail: bool = False,
) -> Callable:
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            process = psutil.Process()
            mem_usage = []

            def monitor():
                while monitoring:
                    current_mem = process.memory_info().rss / 1024 / 1024
                    mem_usage.append(current_mem)
                    time.sleep(interval)

            monitoring = True
            thread = threading.Thread(target=monitor, daemon=True)
            thread.start()

            try:
                result = func(*args, **kwargs)
            finally:
                monitoring = False
                thread.join()

            print_ram_usage(mem_usage, interval, func.__name__, is_detail)

            return result

        return wrapper

    return decorator
