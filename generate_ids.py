import uuid
from typing import List, Any, Generator

from performance_monitoring.timer import timer_of_execution

def generate_uuids(num_of_ids: int) -> Generator[str, Any, None]:
    for _ in range(num_of_ids):
        yield uuid.uuid4().hex

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