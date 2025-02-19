from collections import deque
from time import sleep
from typing import Union, List, Dict, Set, Iterator

from get_ids import (
    generate_ids_in_list,
    generate_ids_in_set,
    generate_ids_in_deque,
    generate_ids_in_dict,
)
from performance_monitoring.cpu import cpu_monitor_decorator, cpu_usage_results
from performance_monitoring.ram import ram_monitor_decorator, ram_usage_results
from utils.graphs import plot_combined_graph_for_cpu, plot_combined_ram_graph
from utils.redis_test_data_loader import create_list_iterator_from_redis_keys


def benchmark_membership_test(
    collection: Union[List[str], Dict[str, str], set[str], deque[str]],
    list_keys_with_data: List[str],
) -> None:
    for obj in list_keys_with_data:
        if obj in collection:
            continue
        else:
            continue


@ram_monitor_decorator()
@cpu_monitor_decorator()
def analyze_membership_performance(
    collection: Union[List[str], Dict[str, None], Set[str], deque],
    list_keys_with_data: List[str],
    **kwargs,
) -> None:
    benchmark_membership_test(
        collection=collection,
        list_keys_with_data=list_keys_with_data,
    )


def run_membership_benchmark(
    list_iterator: List[Iterator[bytes]], list_keys_with_data: List[str]
) -> None:
    iter_1, iter_2, iter_3, iter_4 = list_iterator

    list_ids = generate_ids_in_list(iter_1)
    deque_ids = generate_ids_in_deque(iter_2)
    set_ids = generate_ids_in_set(iter_3)
    dict_ids = generate_ids_in_dict(iter_4)
    sleep(2)

    analyze_membership_performance(
        collection=list_ids,
        list_keys_with_data=list_keys_with_data,
        func_name="Membership performance for List",
    )
    sleep(1)

    analyze_membership_performance(
        collection=deque_ids,
        list_keys_with_data=list_keys_with_data,
        func_name="Membership performance for Deque",
    )
    sleep(1)

    analyze_membership_performance(
        collection=set_ids,
        list_keys_with_data=list_keys_with_data,
        func_name="Membership performance for Set",
    )
    sleep(1)

    analyze_membership_performance(
        collection=dict_ids,
        list_keys_with_data=list_keys_with_data,
        func_name="Membership performance for Dict",
    )
    sleep(1)


def main_benchmark_membership(list_keys: List[str], repeat: int = 10) -> None:
    for _ in range(repeat):
        run_membership_benchmark(
            list_keys_with_data=list_keys,
            list_iterator=create_list_iterator_from_redis_keys(),
        )

    plot_combined_graph_for_cpu(cpu_data=cpu_usage_results)
    plot_combined_ram_graph(ram_data=ram_usage_results)
