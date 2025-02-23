from collections import deque
from typing import List, Any, Dict, Set, Type, Union

from pympler import asizeof

from performance_monitoring.cpu import cpu_monitor_decorator
from performance_monitoring.ram import ram_monitor_decorator
from utils.redis_for_save_usage_data import usage_r_client
from utils.redis_test_data_loader import (
    fetch_data_from_redis_for_structure,
)


@cpu_monitor_decorator(r_client=usage_r_client)
@ram_monitor_decorator(r_client=usage_r_client)
def load_data_to_collection_from_redis(
    data_structure: Type[Union[list, deque, dict, set]],
    **kwargs,
) -> Union[
    List[dict[str, Any]], deque[Dict[str, Any]], Dict[str, Any], Set[bytes]
]:
    return fetch_data_from_redis_for_structure(data_structure=data_structure)


def run_benchmark_create_collections_real_data(num_test: int) -> None:
    data_for_benchmark = {
        1: (list, "Create List with real data"),
        2: (deque, "Create Deque with real data"),
        3: (set, "Create Set with real data"),
        4: (dict, "Create Dict with real data"),
    }

    collection = load_data_to_collection_from_redis(
        data_structure=data_for_benchmark[num_test][0],
        func_name=data_for_benchmark[num_test][1],
    )

    print(
        f"Size of {data_for_benchmark[num_test][1]}: "
        f"{asizeof.asizeof(collection) / 1024 / 1024:.2f} MB"
    )


if __name__ == "__main__":
    run_benchmark_create_collections_real_data(num_test=3)
