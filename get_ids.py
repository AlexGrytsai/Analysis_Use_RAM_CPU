from collections import deque
from typing import List, Dict, Generator, Any, Iterator

from utils.uuid_generator import generate_uuids


def generate_ids_in_list(
    redis_iterator: Iterator[bytes],
) -> List[str]:
    ids_list = []
    for uid in redis_iterator:
        ids_list.append(uid.decode())
    return ids_list


def generate_ids_in_set(
    redis_iterator: Iterator[bytes],
) -> set[bytes]:
    ids_set = set()
    for uid in redis_iterator:
        ids_set.add(uid)
    return ids_set


def generate_ids_in_deque(
    redis_iterator: Iterator[bytes],
) -> deque[str]:
    ids_deque = deque([])
    for uid in redis_iterator:
        ids_deque.append(uid.decode())
    return ids_deque


def generate_ids_in_dict(
    redis_iterator: Iterator[bytes],
) -> Dict[str, None]:
    ids_dict = {}
    for uid in redis_iterator:
        ids_dict[uid.decode()] = None
    return ids_dict
