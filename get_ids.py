from typing import List

from performance_monitoring.timer import timer_of_execution
from utils.uuid_generator import generate_uuids


@timer_of_execution
def generate_ids_in_list(num_of_ids: int) -> List[str]:
    ids_list = []
    for uid in generate_uuids(num_of_ids):
        ids_list.append(uid)
    return ids_list


@timer_of_execution
def generate_ids_in_set(num_of_ids: int) -> set[str]:
    ids_set = set()
    for uid in generate_uuids(num_of_ids):
        ids_set.add(uid)
    return ids_set
