from collections import deque
from typing import List, Dict, Iterator, Set


def generate_ids_in_list(
    redis_iterator: Iterator[str],
) -> List[str]:
    ids_list = []
    for uid in redis_iterator:
        ids_list.append(uid)
    return ids_list


def generate_ids_in_set(
    redis_iterator: Iterator[str],
) -> Set[str]:
    ids_set = set()
    for uid in redis_iterator:
        ids_set.add(uid)
    return ids_set


def generate_ids_in_deque(
    redis_iterator: Iterator[str],
) -> deque[str]:
    ids_deque = deque([])
    for uid in redis_iterator:
        ids_deque.append(uid)
    return ids_deque


def generate_ids_in_dict(
    redis_iterator: Iterator[str],
) -> Dict[str, None]:
    ids_dict = {}
    for uid in redis_iterator:
        ids_dict[uid] = None
    return ids_dict
