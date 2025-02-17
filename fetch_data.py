from collections import deque
from typing import List, Any, Dict

from performance_monitoring.timer import timer_of_execution
from utils.get_test_data import get_test_data_from_json


@timer_of_execution
def add_test_data_to_list(file_path: str) -> List[dict[str, Any]]:
    data_list = []
    for data in get_test_data_from_json(file_path):
        data_list.append(data)
    return data_list


@timer_of_execution
def add_test_data_to_set(file_path: str) -> set[Dict[str, Any]] | None:
    data_set = set()
    for data in get_test_data_from_json(file_path):
        try:
            data_set.add(data)
        except TypeError as exc:
            print(f"⛔ Set does not support {type(data)}: {exc}")
            break
    return data_set if data_set else None


@timer_of_execution
def add_test_data_to_deque(file_path: str) -> deque[Dict[str, Any]]:
    data_deque = deque([])
    for data in get_test_data_from_json(file_path):
        data_deque.append(data)
    return data_deque
