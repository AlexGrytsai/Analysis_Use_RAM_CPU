from collections import deque
from typing import Union, Callable, Iterator

from performance_monitoring.cpu import cpu_monitor_decorator
from performance_monitoring.memory import memory_object_report
from performance_monitoring.ram import ram_monitor_decorator
from utils.get_ids import (
    generate_ids_in_list,
    generate_ids_in_deque,
    generate_ids_in_set,
    generate_ids_in_dict,
)
from utils.redis_for_save_usage_data import usage_r_client
from utils.redis_test_data_loader import (
    redis_client,
)


@cpu_monitor_decorator(r_client=usage_r_client, is_enabled=True)
@ram_monitor_decorator(r_client=usage_r_client, is_enabled=True)
def measure_resource_usage(
    redis_iterator: Iterator[bytes],
    func: Callable,
    **kwargs,
) -> Union[list, dict, set, deque]:
    ids_collection = func(redis_iterator)
    if kwargs.get("memory_report", True):
        memory_object_report(ids_collection)
    return ids_collection


if __name__ == "__main__":
    """
    func:
        - generate_ids_in_list -> Generate IDs in List
        - generate_ids_in_deque -> Generate IDs in Deque
        - generate_ids_in_set -> Generate IDs in Set
        - generate_ids_in_dict -> Generate IDs in Dict
    """
    measure_resource_usage(
        func=generate_ids_in_list,
        redis_iterator=redis_client.scan_iter("*"),
        func_name="Generate IDs in List",
        memory_report=False,
    )
