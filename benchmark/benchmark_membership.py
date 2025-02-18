import random
from collections import deque
from time import sleep
from typing import Union, List, Dict, Set

from get_ids import (
    generate_ids_in_list,
    generate_ids_in_set,
    generate_ids_in_deque,
    generate_ids_in_dict,
)
from performance_monitoring.cpu import cpu_monitor_decorator
from performance_monitoring.ram import ram_monitor_decorator


def generate_search_samples(
    dataset: Union[List[str], Dict[str, str], Set[str], deque],
    num_samples: int,
) -> List[str]:
    if isinstance(dataset, dict):
        dataset = list(dataset.keys())

    elif isinstance(dataset, set):
        dataset = list(dataset)

    return [random.choice(dataset) for _ in range(num_samples)]


def benchmark_membership_test(
    collection: Union[List[str], Dict[str, str], set[str], deque[str]],
    search_samples: List[str],
) -> None:
    for obj in search_samples:
        if obj in collection:
            continue
        else:
            continue


@ram_monitor_decorator()
@cpu_monitor_decorator()
def analyze_membership_performance(
    collection: Union[List[str], Dict[str, str], Set[str], deque],
    search_samples: Union[List[str], Dict[str, str], Set[str], deque],
    **kwargs,
) -> None:
    benchmark_membership_test(
        collection=collection,
        search_samples=search_samples,
    )


def run_membership_benchmark(num_ids: int, num_searches: int) -> None:
    list_ids = generate_ids_in_list(num_ids)
    search_samples_list = generate_search_samples(list_ids, num_searches)

    deque_ids = generate_ids_in_deque(num_ids)
    search_samples_deque = generate_search_samples(deque_ids, num_searches)

    set_ids = generate_ids_in_set(num_ids)
    search_samples_set = generate_search_samples(set_ids, num_searches)

    dict_ids = generate_ids_in_dict(num_ids)
    search_samples_dict = generate_search_samples(dict_ids, num_searches)
    sleep(2)

    analyze_membership_performance(
        collection=list_ids,
        search_samples=search_samples_list,
        func_name="Membership performance analysis for List",
    )
    sleep(1)

    analyze_membership_performance(
        collection=deque_ids,
        search_samples=search_samples_deque,
        func_name="Membership performance analysis for Deque",
    )
    sleep(1)

    analyze_membership_performance(
        collection=set_ids,
        search_samples=search_samples_set,
        func_name="Membership performance analysis for Set",
    )
    sleep(1)

    analyze_membership_performance(
        collection=dict_ids,
        search_samples=search_samples_dict,
        func_name="Membership performance analysis for Dict",
    )
    sleep(1)
