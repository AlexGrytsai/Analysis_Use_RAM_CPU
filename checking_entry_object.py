import random
import uuid
from collections import deque
from typing import List, Union, Dict

from performance_monitoring.timer import timer_of_execution


def generation_list_of_objects_for_search(
    full_list_ids: List[str], num_of_objects: int
) -> List[str]:
    list_of_objects = []
    for _ in range(num_of_objects):
        list_of_objects.append(
            full_list_ids[random.randint(0, len(full_list_ids) - 1)]
        )
    return list_of_objects


@timer_of_execution
def check_entry_object_in_list(
    list_of_objects: Union[List[str], Dict[str, str], set[str], deque[str]],
    number_of_checks: int,
) -> None:
    list_for_check = generation_list_of_objects_for_search(
        list_of_objects, number_of_checks
    )
    for obj in list_for_check:
        if obj in list_of_objects:
            continue
        else:
            continue


@timer_of_execution
def check_entry_object_in_set(
    set_of_objects: set,
    number_of_checks: int,
) -> None:
    for _ in range(number_of_checks):
        entry_object: str = uuid.uuid4().hex
        if entry_object in set_of_objects:
            continue
        else:
            continue


@timer_of_execution
def check_entry_object_in_deque(
    deque_of_objects: deque,
    number_of_checks: int,
) -> None:
    for _ in range(number_of_checks):
        entry_object: str = uuid.uuid4().hex
        if entry_object in deque_of_objects:
            continue
        else:
            continue


@timer_of_execution
def check_entry_object_in_dict(
    dict_of_objects: dict,
    number_of_checks: int,
) -> None:
    for _ in range(number_of_checks):
        entry_object: str = uuid.uuid4().hex
        if entry_object in dict_of_objects:
            continue
        else:
            continue
