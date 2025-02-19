import json
from collections import deque
from time import sleep
from typing import List, Any, Dict, Set

from redis import Redis

from benchmark.benchmark_data_structures import (
    fetch_data_from_redis_for_structure,
)
from performance_monitoring.cpu import cpu_monitor_decorator
from performance_monitoring.memory import memory_object_report
from performance_monitoring.ram import ram_monitor_decorator
from utils.validators import TenderDataValidator


@ram_monitor_decorator()
@cpu_monitor_decorator()
def validate_data_from_list(
    raw_data_list: List[Dict[str, Any]],
) -> List[TenderDataValidator]:
    clean_data = []
    for data in raw_data_list:
        validate_date = TenderDataValidator(**data)
        clean_data.append(validate_date)
    return clean_data


@ram_monitor_decorator()
@cpu_monitor_decorator()
def validate_data_from_deque(
    raw_data_deque: deque,
) -> deque[TenderDataValidator]:
    clean_data = deque([])
    for data in raw_data_deque:
        validate_date = TenderDataValidator(**data)
        clean_data.append(validate_date)
    return clean_data


@ram_monitor_decorator()
@cpu_monitor_decorator()
def validate_data_from_dict(
    raw_data_dict: Dict[str, Any],
) -> Dict[str, TenderDataValidator]:
    clean_data = {}
    for key, value in raw_data_dict.items():
        validate_date = TenderDataValidator(**value)
        clean_data[key] = validate_date
    return clean_data


@ram_monitor_decorator()
@cpu_monitor_decorator()
def validate_data_from_set(
    raw_data_set: Set,
) -> Set[str]:
    clean_data = set()
    for value in raw_data_set:
        clean_data.add(
            TenderDataValidator(**json.loads(value)).model_dump_json()
        )
    return clean_data


def benchmark_validate_data(
    redis_keys: List[str],
    redis_client: Redis,
    memory_report: bool = False,
) -> None:
    validated_data_from_list = validate_data_from_list(
        raw_data_list=fetch_data_from_redis_for_structure(
            redis_keys, redis_client, list
        )
    )
    sleep(1)

    validated_data_from_deque = validate_data_from_deque(
        raw_data_deque=fetch_data_from_redis_for_structure(
            redis_keys, redis_client, deque
        )
    )
    sleep(1)

    validated_data_from_dict = validate_data_from_dict(
        raw_data_dict=fetch_data_from_redis_for_structure(
            redis_keys, redis_client, dict
        )
    )
    validated_data_from_set = validate_data_from_set(
        raw_data_set=fetch_data_from_redis_for_structure(
            redis_keys, redis_client, set
        )
    )
    sleep(1)

    if memory_report:
        memory_object_report(validated_data_from_list)
        memory_object_report(validated_data_from_deque)
        memory_object_report(validated_data_from_dict)
        memory_object_report(validated_data_from_set)
