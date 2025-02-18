import random
from collections import deque
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
    print(
        f"Checking in {type(collection)}. "
        f"Need to check {len(search_samples)}"
    )
    for obj in search_samples:
        if obj in collection:
            continue
        else:
            continue


@ram_monitor_decorator()
@cpu_monitor_decorator()
def analyze_membership_performance(
    collection: Union[List[str], Dict[str, str], Set[str], deque],
    num_searches: int,
) -> None:
    benchmark_membership_test(
        collection=collection,
        search_samples=generate_search_samples(
            collection, num_searches
        ),
    )


def run_membership_benchmark(num_ids: int, num_checks: int) -> None:
    analyze_membership_performance(
        collection=generate_ids_in_list(num_ids), num_searches=num_checks
    )
    analyze_membership_performance(
        collection=generate_ids_in_deque(num_ids), num_searches=num_checks
    )
    analyze_membership_performance(
        collection=generate_ids_in_set(num_ids), num_searches=num_checks
    )
    analyze_membership_performance(
        collection=generate_ids_in_dict(num_ids), num_searches=num_checks
    )
