from collections import deque
from typing import List, Dict

from performance_monitoring.cpu import cpu_monitor_decorator
from performance_monitoring.ram import ram_monitor_decorator
from utils.uuid_generator import generate_uuids


@ram_monitor_decorator()
@cpu_monitor_decorator
def generate_ids_in_list(num_of_ids: int) -> List[str]:
    ids_list = []
    for uid in generate_uuids(num_of_ids):
        ids_list.append(uid)
    return ids_list


@ram_monitor_decorator()
@cpu_monitor_decorator
def generate_ids_in_set(num_of_ids: int) -> set[str]:
    ids_set = set()
    for uid in generate_uuids(num_of_ids):
        ids_set.add(uid)
    return ids_set


@ram_monitor_decorator()
@cpu_monitor_decorator
def generate_ids_in_deque(num_of_ids: int) -> deque[str]:
    ids_deque = deque([])
    for uid in generate_uuids(num_of_ids):
        ids_deque.append(uid)
    return ids_deque


@ram_monitor_decorator()
@cpu_monitor_decorator
def generate_ids_in_dict(num_of_ids: int) -> Dict[str, str]:
    ids_dict = {}
    for uid in generate_uuids(num_of_ids):
        ids_dict[uid] = uid
    return ids_dict
