import functools
import threading
import time
from typing import Callable

import psutil
from matplotlib import pyplot as plt

running = False
cpu_usage_data = []


def monitor_cpu_usage(interval=0.1):
    global running, cpu_usage_data
    cpu_usage_data = []
    while running:
        cpu_usage_data.append(psutil.cpu_percent(interval=interval))


def make_graph_for_cpu(cpu_usage: list, func_name: str) -> None:
    plt.figure(figsize=(10, 6))
    plt.plot(
        [i * 0.1 for i in range(len(cpu_usage))],
        cpu_usage_data,
        marker="o",
        color="r",
        label="CPU Usage (%)",
    )
    plt.title(f"CPU Usage for Function: {func_name}")
    plt.xlabel("Time (seconds)")
    plt.ylabel("CPU Usage (%)")
    plt.grid(True)
    plt.legend()
    plt.show()


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

        print(f"\n📊 CPU Usage Report for '{func.__name__}':")
        print(f"  🕒 Execution time: {end_time - start_time:.4f} seconds")
        print(f"  ⚡ Average CPU Load: {avg_cpu:.2f}%")
        print(f"  🚀 Peak CPU Load: {max_cpu:.2f}%\n")

        make_graph_for_cpu(cpu_usage=cpu_usage_data, func_name=func.__name__)

        return result

    return wrapper
