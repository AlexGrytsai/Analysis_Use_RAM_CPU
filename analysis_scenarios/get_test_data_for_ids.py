import uuid
from collections import deque
from typing import List, Any, Dict

from performance_monitoring.cpu import cpu_monitor_decorator
from performance_monitoring.memory import memory_object_report
from performance_monitoring.ram import ram_monitor_decorator
from utils.get_test_data import get_test_data_from_json


def add_test_data_to_list(
    file_path: str, num_of_ids: int
) -> List[dict[str, Any]]:
    data_list = []
    for data in get_test_data_from_json(file_path, num_of_ids):
        data_list.append(data)
    return data_list


def add_test_data_to_set(
    file_path: str, num_of_ids: int
) -> set[Dict[str, Any]] | None:
    data_set = set()
    for data in get_test_data_from_json(file_path, num_of_ids):
        try:
            data_set.add(data)
        except TypeError as exc:
            print(f"⛔ Set does not support {type(data)}: {exc}")
            break
    return data_set if data_set else None


def add_test_data_to_deque(
    file_path: str, num_of_ids: int
) -> deque[Dict[str, Any]]:
    data_deque = deque([])
    for data in get_test_data_from_json(file_path, num_of_ids):
        data_deque.append(data)
    return data_deque


def add_test_data_to_dict(file_path: str, num_of_ids: int) -> Dict[str, Any]:
    data_dict = {}
    for data in get_test_data_from_json(file_path, num_of_ids):
        data_dict[uuid.uuid4().hex] = data
    return data_dict


def main_analyze_creation_test_data(file_path: str, num_of_ids: int) -> None:
    data_in_list = ram_monitor_decorator(is_detail=False)(
        cpu_monitor_decorator(add_test_data_to_list)(file_path, num_of_ids)
    )
    memory_object_report(data_in_list)

    data_in_deque = ram_monitor_decorator(is_detail=False)(
        cpu_monitor_decorator(add_test_data_to_deque)(file_path, num_of_ids)
    )
    memory_object_report(data_in_deque)

    data_in_set = ram_monitor_decorator(is_detail=False)(
        cpu_monitor_decorator(add_test_data_to_set)(file_path, num_of_ids)
    )
    memory_object_report(data_in_set)

    data_in_dict = ram_monitor_decorator(is_detail=False)(
        cpu_monitor_decorator(add_test_data_to_dict)(file_path, num_of_ids)
    )
    memory_object_report(data_in_dict)
