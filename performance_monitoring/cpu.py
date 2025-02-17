import functools
import threading
import time
from typing import Callable

import psutil

from utils.graphs import make_graph_for_cpu

running = False
cpu_usage_data = []


def monitor_cpu_usage(interval=0.1):
    global running, cpu_usage_data
    cpu_usage_data = []
    while running:
        cpu_usage_data.append(psutil.cpu_percent(interval=interval))


def cpu_monitor_decorator(func: Callable) -> Callable:
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        global running
        running = True
        cpu_thread = threading.Thread(target=monitor_cpu_usage, daemon=True)
        cpu_thread.start()

        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()

        running = False
        cpu_thread.join()

        avg_cpu = (
            sum(cpu_usage_data) / len(cpu_usage_data) if cpu_usage_data else 0
        )
        max_cpu = max(cpu_usage_data, default=0)
        exec_time = end_time - start_time

        print(f"\n📊 CPU Usage Report for '{func.__name__}':")
        print(f"  🕒 Execution time: {exec_time:.4f} seconds")
        print(f"  ⚡ Average CPU Load: {avg_cpu:.2f}%")
        print(f"  🚀 Peak CPU Load: {max_cpu:.2f}%\n")

        make_graph_for_cpu(
            cpu_usage=cpu_usage_data,
            func_name=func.__name__,
            exec_time=exec_time,
            avg_cpu=avg_cpu,
            max_cpu=max_cpu,
        )

        return result

    return wrapper
