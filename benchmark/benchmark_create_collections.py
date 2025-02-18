from collections import deque
from time import sleep
from typing import Union

from get_ids import (
    generate_ids_in_list,
    generate_ids_in_set,
    generate_ids_in_deque,
    generate_ids_in_dict,
)
from performance_monitoring.cpu import cpu_monitor_decorator
from performance_monitoring.memory import memory_object_report
from performance_monitoring.ram import ram_monitor_decorator


def measure_resource_usage(
    generator,
    num_ids: int,
    graph: bool = False,
    **kwargs,
) -> Union[list, dict, set, deque]:
    return ram_monitor_decorator(plot_graph=graph)(
        cpu_monitor_decorator()(generator)
    )(num_ids)


def benchmark_id_generation(num_ids: int, graph: bool = False) -> None:
    ids_list = measure_resource_usage(
        generator=generate_ids_in_list,
        num_ids=num_ids,
        graph=graph,
        func_name="Generate IDs in List",
    )
    memory_object_report(ids_list)
    sleep(1)

    ids_deque = measure_resource_usage(
        generator=generate_ids_in_deque,
        num_ids=num_ids,
        graph=graph,
        func_name="Generate IDs in Deque",
    )
    memory_object_report(ids_deque)
    sleep(1)

    ids_set = measure_resource_usage(
        generator=generate_ids_in_set,
        num_ids=num_ids,
        graph=graph,
        func_name="Generate IDs in Set",
    )
    memory_object_report(ids_set)
    sleep(1)

    ids_dict = measure_resource_usage(
        generator=generate_ids_in_dict,
        num_ids=num_ids,
        graph=graph,
        func_name="Generate IDs in Dict",
    )
    memory_object_report(ids_dict)
    sleep(1)
