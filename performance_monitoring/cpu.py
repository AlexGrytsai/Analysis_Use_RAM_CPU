import functools
import json
import threading
import time
from typing import Callable, List, Tuple, Optional

import psutil
from redis import Redis

running = False
cpu_usage_data = []
cpu_usage_results = {}


def monitor_cpu_usage(interval: float = 0.1):
    global running, cpu_usage_data
    local_cpu_usage = []

    psutil.cpu_percent(interval=None)
    while running:
        local_cpu_usage.append(psutil.cpu_percent(interval=interval))

    cpu_usage_data.extend(local_cpu_usage)


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
    r_client: Optional[Redis] = None,
) -> None:
    if r_client:
        try:
            r_client.set(func_name, json.dumps(cpu_data))
        except Exception as exc:
            raise Exception(f"Failed to save CPU usage data to Redis: {exc}")
    if func_name not in cpu_usage_results:
        cpu_usage_results[func_name] = []
    cpu_usage_results[func_name].append(cpu_data)


def cpu_monitor_decorator(
    to_console: bool = False,
    save_data: bool = True,
    is_enabled: bool = True,
    r_client: Optional[Redis] = None,
) -> Callable:
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if not is_enabled:
                return func(*args, **kwargs)

            global running, cpu_usage_data

            cpu_usage_data = []
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
                    func_name=kwargs.get("func_name", func.__name__),
                    cpu_data=(cpu_usage_data, end_time - start_time),
                    r_client=r_client,
                )

            return result

        return wrapper

    return decorator
