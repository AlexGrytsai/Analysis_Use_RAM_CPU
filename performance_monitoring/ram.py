import functools
import threading
import time
from typing import Callable

import psutil
from matplotlib import pyplot as plt


def make_graph(mem_usage, interval, func_name):
    plt.figure(figsize=(10, 6))
    plt.plot(
        [i * interval for i in range(len(mem_usage))],
        mem_usage,
        marker="o",
        color="b",
        label="RAM Usage (MB)",
    )
    plt.title(f"RAM Usage for Function: {func_name}")
    plt.xlabel("Time (seconds)")
    plt.ylabel("RAM Usage (MB)")
    plt.grid(True)
    plt.legend()
    plt.show()


def print_ram_usage(
    mem_usage: list, interval: float, func_name: str, is_detail: bool
) -> None:
    print(f"📊 Using RAM in the process of performing a '{func_name}':")
    if is_detail:
        for i, usage in enumerate(mem_usage):
            print(f"  Time {i * interval:.2f} seconds: {usage:.2f} MB")

    max_mem = max(mem_usage) if mem_usage else 0
    print(f"  📊 Peak use RAM: {max_mem:.2f} MB")


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
            # make_graph(mem_usage, interval, func.__name__)

            return result

        return wrapper

    return decorator
