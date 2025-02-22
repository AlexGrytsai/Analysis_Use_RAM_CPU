from collections import deque
from typing import Union, Callable, Iterator, Optional

from performance_monitoring.cpu import cpu_monitor_decorator
from performance_monitoring.memory import memory_object_report
from performance_monitoring.ram import ram_monitor_decorator
from utils.get_ids import generate_ids_in_list
from utils.redis_test_data_loader import (
    redis_client,
)


@ram_monitor_decorator()
@cpu_monitor_decorator()
def measure_resource_usage(
    redis_iterator: Iterator[bytes],
    func: Callable,
    **kwargs,
) -> Union[list, dict, set, deque]:
    return func(redis_iterator)


def benchmark_id_generation(
    func: Callable,
    func_name: str,
    iterator: Iterator[bytes],
    memory_report: Optional[bool] = False,
) -> None:
    ids_collection = measure_resource_usage(
        func=func,
        redis_iterator=iterator,
        func_name=func_name,
    )

    if memory_report:
        memory_object_report(ids_collection)


def main_benchmark_ids_generation(
    func: Callable, func_name: str, repeat: int = 2
) -> None:
    for _ in range(repeat):
        benchmark_id_generation(
            func=func,
            func_name=func_name,
            iterator=redis_client.scan_iter("*"),
            memory_report=False,
        )


if __name__ == "__main__":
    """
    func:
        - generate_ids_in_list -> Generate IDs in List
        - generate_ids_in_deque -> Generate IDs in Deque
        - generate_ids_in_set -> Generate IDs in Set
        - generate_ids_in_dict -> Generate IDs in Dict
    """
    main_benchmark_ids_generation(
        func=generate_ids_in_list, func_name="Generate IDs in List"
    )
