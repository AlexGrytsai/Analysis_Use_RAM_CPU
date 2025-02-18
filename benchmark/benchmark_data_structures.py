import uuid
from collections import deque
from time import sleep
from typing import List, Any, Dict, Union, Type, Set

from redis import Redis

from performance_monitoring.cpu import cpu_monitor_decorator
from performance_monitoring.memory import memory_object_report
from performance_monitoring.ram import ram_monitor_decorator


def fetch_data_from_redis_for_structure(
    key_list: List[str],
    redis_client: Redis,
    data_structure: Type[Union[list, deque, dict, set]],
) -> Union[
    List[dict[str, Any]], deque[Dict[str, Any]], Dict[str, Any], Set[bytes]
]:
    if data_structure is list:
        return [redis_client.get(key).decode() for key in key_list]

    elif data_structure is deque:
        return deque(redis_client.get(key).decode() for key in key_list)

    elif data_structure is set:
        return {redis_client.get(key) for key in key_list}

    elif data_structure is dict:
        return {
            uuid.uuid4().hex: redis_client.get(key).decode()
            for key in key_list
        }

    raise ValueError(f"Unsupported data structure: {data_structure}")


@ram_monitor_decorator()
@cpu_monitor_decorator()
def load_list_from_redis(
    key_list: List[str],
    redis_client: Redis,
) -> List[dict[str, Any]]:
    return fetch_data_from_redis_for_structure(key_list, redis_client, list)


@ram_monitor_decorator()
@cpu_monitor_decorator()
def load_deque_from_redis(
    key_list: List[str],
    redis_client: Redis,
) -> deque[Dict[str, Any]]:
    return fetch_data_from_redis_for_structure(key_list, redis_client, deque)


@ram_monitor_decorator()
@cpu_monitor_decorator()
def load_dict_from_redis(
    key_list: List[str],
    redis_client: Redis,
) -> Dict[str, Any]:
    return fetch_data_from_redis_for_structure(key_list, redis_client, dict)


@ram_monitor_decorator()
@cpu_monitor_decorator()
def load_set_from_redis(
    key_list: List[str],
    redis_client: Redis,
) -> Set[bytes]:
    return fetch_data_from_redis_for_structure(key_list, redis_client, set)


def benchmark_data_structures(
    redis_keys: List[str],
    redis_client: Redis,
    memory_report: bool = False,
) -> None:
    data_structures = {
        "List": load_list_from_redis,
        "Deque": load_deque_from_redis,
        "Dict": load_dict_from_redis,
        "Set": load_set_from_redis,
    }

    loaded_data = {}
    for name, func in data_structures.items():
        loaded_data[name] = func(
            key_list=redis_keys, redis_client=redis_client
        )
        sleep(1)

    if memory_report:
        for _, data in loaded_data.items():
            memory_object_report(data)
