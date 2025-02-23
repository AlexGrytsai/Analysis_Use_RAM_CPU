from collections import deque
from typing import Union, Callable, Iterator

from pympler import asizeof

from performance_monitoring.cpu import cpu_monitor_decorator
from performance_monitoring.ram import ram_monitor_decorator
from utils.get_ids import (
    generate_ids_in_list,
    generate_ids_in_deque,
    generate_ids_in_set,
    generate_ids_in_dict,
)
from utils.redis_for_save_usage_data import usage_r_client
from utils.redis_test_data_loader import r_client_prepare


@cpu_monitor_decorator(r_client=usage_r_client, is_enabled=True)
@ram_monitor_decorator(r_client=usage_r_client, is_enabled=True)
def create_collection_with_simple_data(
    func: Callable,
    redis_iterator: Iterator[str] = r_client_prepare.scan_iter("*"),
    **kwargs,
) -> Union[list, dict, set, deque]:
    return func(redis_iterator)


def run_benchmark_simple_collections(
    num_test: int,
) -> None:
    data_for_benchmark = {
        1: (generate_ids_in_list, "Generate IDs in List"),
        2: (generate_ids_in_deque, "Generate IDs in Deque"),
        3: (generate_ids_in_set, "Generate IDs in Set"),
        4: (generate_ids_in_dict, "Generate IDs in Dict"),
    }

    ids_collection = create_collection_with_simple_data(
        func=data_for_benchmark[num_test][0],
        func_name=data_for_benchmark[num_test][1],
    )

    print(
        f"Size of {data_for_benchmark[num_test][1]}: "
        f"{asizeof.asizeof(ids_collection) / 1024:.2f} KB"
    )


if __name__ == "__main__":
    run_benchmark_simple_collections(1)
