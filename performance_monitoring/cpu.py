import functools
import threading
import time
from typing import Callable, List, Tuple

import psutil

running = False
cpu_usage_data = []
cpu_usage_results = {}


def monitor_cpu_usage(interval: float = 0.1):
    global running, cpu_usage_data
    while running:
        cpu_usage_data.append(psutil.cpu_percent(interval=interval))


def print_cpu_analytics_to_console(
    func_name: str,
    exec_time: float,
    cpu_data: List[float],
) -> None:
    avg_cpu = sum(cpu_data) / len(cpu_data) if cpu_data else 0
    max_cpu = max(cpu_data, default=0)

    print(f"\n📊 CPU Usage Report for '{func_name}':")
    print(f"  🕒 Execution time: {exec_time:.4f} seconds")
    print(f"  ⚡ Average CPU Load: {avg_cpu:.2f}%")
    print(f"  🚀 Peak CPU Load: {max_cpu:.2f}%\n")


def save_data_to_usage_results(
    func_name: str,
    cpu_data: Tuple[List[float], float],
) -> None:
    if func_name not in cpu_usage_results:
        cpu_usage_results[func_name] = []
    cpu_usage_results[func_name].append(cpu_data)


def cpu_monitor_decorator(
    to_console: bool = False,
    save_data: bool = True,
    is_enabled: bool = True,
) -> Callable:
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if not is_enabled:
                return func(*args, **kwargs)
            global running
            running = True
            cpu_thread = threading.Thread(
                target=monitor_cpu_usage, daemon=True
            )
            cpu_thread.start()

            start_time = time.perf_counter()
            result = func(*args, **kwargs)
            end_time = time.perf_counter()

            running = False
            cpu_thread.join()
            if to_console:
                print_cpu_analytics_to_console(
                    func_name=kwargs.get("func_name", func.__name__),
                    exec_time=(end_time - start_time),
                    cpu_data=cpu_usage_data,
                )

            if save_data:
                save_data_to_usage_results(
                    kwargs.get("func_name", func.__name__),
                    (cpu_usage_data, end_time - start_time),
                )

            return result

        return wrapper

    return decorator
