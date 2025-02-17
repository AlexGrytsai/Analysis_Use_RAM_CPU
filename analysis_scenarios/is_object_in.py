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
from performance_monitoring.timer import timer_of_execution


def generation_list_of_objects_for_search(
    full_list_ids: Union[List[str], Dict[str, str], Set[str], deque],
    num_of_objects: int,
) -> List[str]:
    list_of_objects = []

    if isinstance(full_list_ids, dict):
        full_list_ids = list(full_list_ids.keys())

    elif isinstance(full_list_ids, set):
        full_list_ids = list(full_list_ids)

    for _ in range(num_of_objects):
        list_of_objects.append(random.choice(full_list_ids))

    return list_of_objects


def check_entry_object_in_list(
    list_of_objects: Union[List[str], Dict[str, str], set[str], deque[str]],
    list_for_check: List[str],
) -> None:
    print(
        f"Checking in {type(list_of_objects)}. "
        f"Need to check {len(list_for_check)}"
    )
    for obj in list_for_check:
        if obj in list_of_objects:
            continue
        else:
            continue


@ram_monitor_decorator()
@cpu_monitor_decorator
def analyze_check_is_object_in_(
    list_of_ids: Union[List[str], Dict[str, str], Set[str], deque],
    num_checks: int,
) -> None:
    check_entry_object_in_list(
        list_of_objects=list_of_ids,
        list_for_check=generation_list_of_objects_for_search(
            list_of_ids, num_checks
        ),
    )


def main_analyze_check_is_object_in_(num_ids: int, num_checks: int) -> None:
    analyze_check_is_object_in_(
        list_of_ids=generate_ids_in_list(num_ids), num_checks=num_checks
    )
    analyze_check_is_object_in_(
        list_of_ids=generate_ids_in_deque(num_ids), num_checks=num_checks
    )
    analyze_check_is_object_in_(
        list_of_ids=generate_ids_in_set(num_ids), num_checks=num_checks
    )
    analyze_check_is_object_in_(
        list_of_ids=generate_ids_in_dict(num_ids), num_checks=num_checks
    )
