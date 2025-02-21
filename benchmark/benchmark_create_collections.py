from collections import deque
from time import sleep
from typing import Union, Callable, Iterator, List

from performance_monitoring.cpu import cpu_monitor_decorator, cpu_usage_results
from performance_monitoring.memory import memory_object_report
from performance_monitoring.ram import ram_monitor_decorator, ram_usage_results
from utils.get_ids import (
    generate_ids_in_list,
    generate_ids_in_set,
    generate_ids_in_deque,
    generate_ids_in_dict,
)
from utils.graphs import plot_combined_graph_for_cpu, plot_combined_ram_graph
from utils.redis_test_data_loader import create_list_iterator_from_redis_keys


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

    ids_deque = measure_resource_usage(
        func=generate_ids_in_deque,
        redis_iterator=iterator_2,
        func_name="Generate IDs in Deque",
    )

    ids_set = measure_resource_usage(
        func=generate_ids_in_set,
        redis_iterator=iterator_3,
        func_name="Generate IDs in Set",
    )

    ids_dict = measure_resource_usage(
        func=generate_ids_in_dict,
        redis_iterator=iterator_4,
        func_name="Generate IDs in Dict",
    )

    if memory_report:
        memory_object_report(ids_list)
        memory_object_report(ids_deque)
        memory_object_report(ids_set)
        memory_object_report(ids_dict)


def main_benchmark_ids_generation(repeat: int = 1) -> None:
    for _ in range(repeat):
        benchmark_id_generation(
            list_iterator=create_list_iterator_from_redis_keys(),
            memory_report=False,
        )

    plot_combined_graph_for_cpu(cpu_data=cpu_usage_results)
    plot_combined_ram_graph(ram_data=ram_usage_results)
