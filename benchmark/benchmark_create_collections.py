from collections import deque
from time import sleep
from typing import Union, Callable, Iterator, List

from get_ids import (
    generate_ids_in_list,
    generate_ids_in_set,
    generate_ids_in_deque,
    generate_ids_in_dict,
)
from performance_monitoring.cpu import cpu_monitor_decorator
from performance_monitoring.memory import memory_object_report
from performance_monitoring.ram import ram_monitor_decorator


@ram_monitor_decorator()
@cpu_monitor_decorator()
def measure_resource_usage(
    redis_iterator: Iterator[bytes],
    func: Callable,
    **kwargs,
) -> Union[list, dict, set, deque]:
    return func(redis_iterator)


def benchmark_id_generation(
    list_iterator: List[Iterator[bytes]],
    memory_report: bool = False,
) -> None:
    iterator_1, iterator_2, iterator_3, iterator_4 = list_iterator

    ids_list = measure_resource_usage(
        func=generate_ids_in_list,
        redis_iterator=iterator_1,
        func_name="Generate IDs in List",
    )
    sleep(1)

    ids_deque = measure_resource_usage(
        func=generate_ids_in_deque,
        redis_iterator=iterator_2,
        func_name="Generate IDs in Deque",
    )
    sleep(1)

    ids_set = measure_resource_usage(
        func=generate_ids_in_set,
        redis_iterator=iterator_3,
        func_name="Generate IDs in Set",
    )
    sleep(1)

    ids_dict = measure_resource_usage(
        func=generate_ids_in_dict,
        redis_iterator=iterator_4,
        func_name="Generate IDs in Dict",
    )
    sleep(1)

    if memory_report:
        memory_object_report(ids_list)
        memory_object_report(ids_deque)
        memory_object_report(ids_set)
        memory_object_report(ids_dict)
