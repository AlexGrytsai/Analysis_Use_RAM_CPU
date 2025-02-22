import functools
import json
import threading
import time
from typing import Callable, List, Tuple, Optional

import psutil
from redis import Redis

from utils.redis_for_save_usage_data import usage_r_client

monitoring = False
ram_usage = []
ram_usage_results = {}


def save_data_to_usage_results(
    func_name: str,
    ram_data: Tuple[List[float], float],
    r_client: Optional[Redis] = None,
) -> None:
    if r_client:
        try:
            r_client.rpush(f"ram_usage_{func_name}", json.dumps(ram_data))
        except Exception as exc:
            raise Exception(f"Failed to save RAM usage data to Redis: {exc}")
    if func_name not in ram_usage_results:
        ram_usage_results[func_name] = []
    ram_usage_results[func_name].append(ram_data)


def print_ram_usage(
    mem_usage: list,
    interval: float,
    func_name: str,
    is_detail: bool,
) -> None:
    print(f"📊 Using RAM in the process of performing a '{func_name}':")
    if is_detail:
        for i, usage in enumerate(mem_usage):
            print(f"  Time {i * interval:.2f} seconds: {usage:.2f} MB")

    max_mem = max(mem_usage) if mem_usage else 0
    print(f"  📊 Peak use RAM: {max_mem:.2f} MB")


def monitor_ram_usage(interval: float = 0.1) -> None:
    global monitoring, ram_usage
    local_ram_usage = []
    process = psutil.Process()
    while monitoring:
        local_ram_usage.append(process.memory_info().rss / 1024 / 1024)
        time.sleep(interval)

    ram_usage.extend(local_ram_usage)


def ram_monitor_decorator(
    interval: float = 0.1,
    r_client: Optional[Redis] = usage_r_client,
    is_detail: Optional[bool] = False,
    to_console: Optional[bool] = False,
    save_data: Optional[bool] = True,
    is_enabled: Optional[bool] = True,
) -> Callable:
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if not is_enabled:
                return func(*args, **kwargs)

            global monitoring, ram_usage

            ram_usage = []
            monitoring = True

            thread = threading.Thread(target=monitor_ram_usage, daemon=True)
            thread.start()

            try:
                start_time = time.perf_counter()
                result = func(*args, **kwargs)
                end_time = time.perf_counter()
            finally:
                monitoring = False
                thread.join()
            if to_console:
                print_ram_usage(
                    ram_usage,
                    interval,
                    kwargs.get("func_name", func.__name__),
                    is_detail,
                )
            if save_data:
                save_data_to_usage_results(
                    func_name=kwargs.get("func_name", func.__name__),
                    ram_data=(ram_usage, end_time - start_time),
                    r_client=r_client,
                )

            return result

        return wrapper

    return decorator
