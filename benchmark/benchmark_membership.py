from collections import deque
from typing import Union, List, Dict

from benchmark.benchmark_create_collections import (
    create_collection_with_simple_data,
)
from performance_monitoring.cpu import cpu_monitor_decorator
from performance_monitoring.ram import ram_monitor_decorator
from utils.get_ids import (
    generate_ids_in_list,
)
from utils.redis_for_save_usage_data import usage_r_client
from utils.redis_test_data_loader import (
    r_client_prepare,
)


@cpu_monitor_decorator(r_client=usage_r_client)
@ram_monitor_decorator(r_client=usage_r_client)
def benchmark_membership_test(
    collection: Union[List[str], Dict[str, str], set[str], deque[str]],
    list_keys_with_data: List[str],
    **kwargs,
) -> None:
    for obj in list_keys_with_data:
        if obj in collection:
            continue
        else:
            continue


if __name__ == "__main__":
    """
    collection:
        - List IDs -> generate_ids_in_list -> Membership performance for List
        - Deque IDs-> generate_ids_in_deque -> Membership performance for Deque
        - Set IDs -> generate_ids_in_set -> Membership performance for Set
        - Dict IDs -> generate_ids_in_dict -> Membership performance for Dict
    """
    list_ids_with_data = r_client_prepare.lrange("list_keys_with_data", 0, -1)

    ids_collection = create_collection_with_simple_data(
        func=generate_ids_in_list,
        redis_iterator=r_client_prepare.scan_iter("*"),
    )

    benchmark_membership_test(
        collection=ids_collection,
        list_keys_with_data=list_ids_with_data,
        func_name="Membership performance for List",
    )
