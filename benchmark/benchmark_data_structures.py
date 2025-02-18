import uuid
from collections import deque
from typing import List, Any, Dict

from performance_monitoring.cpu import cpu_monitor_decorator
from performance_monitoring.memory import memory_object_report
from performance_monitoring.ram import ram_monitor_decorator
from utils.get_test_data import get_test_data_from_json


@ram_monitor_decorator()
@cpu_monitor_decorator()
def generate_list_from_json(
    file_path: str, num_samples: int
) -> List[dict[str, Any]]:
    data_list = []
    for data in get_test_data_from_json(file_path, num_samples):
        data_list.append(data)
    return data_list


@ram_monitor_decorator()
@cpu_monitor_decorator()
def generate_set_from_json(
    file_path: str, num_samples: int
) -> set[Dict[str, Any]] | None:
    data_set = set()
    for data in get_test_data_from_json(file_path, num_samples):
        try:
            data_set.add(data)
        except TypeError as exc:
            print(f"⛔ Set does not support {type(data)}: {exc}")
            break
    return data_set if data_set else None


@ram_monitor_decorator()
@cpu_monitor_decorator()
def generate_deque_from_json(
    file_path: str, num_samples: int
) -> deque[Dict[str, Any]]:
    data_deque = deque([])
    for data in get_test_data_from_json(file_path, num_samples):
        data_deque.append(data)
    return data_deque


@ram_monitor_decorator()
@cpu_monitor_decorator()
def generate_dict_from_json(
    file_path: str, num_samples: int
) -> Dict[str, Any]:
    data_dict = {}
    for data in get_test_data_from_json(file_path, num_samples):
        data_dict[uuid.uuid4().hex] = data
    return data_dict


def benchmark_data_structures(file_path: str, num_samples: int) -> None:
    data_in_list = generate_list_from_json(file_path, num_samples)
    memory_object_report(data_in_list)

    data_in_deque = generate_deque_from_json(file_path, num_samples)
    memory_object_report(data_in_deque)

    data_in_set = generate_set_from_json(file_path, num_samples)
    memory_object_report(data_in_set)

    data_in_dict = generate_dict_from_json(file_path, num_samples)
    memory_object_report(data_in_dict)
