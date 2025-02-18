from collections import deque
from typing import List, Any, Dict, Set

from performance_monitoring.cpu import cpu_monitor_decorator
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
        validate_date = TenderDataValidator(**value.decode())
        clean_data.add(validate_date.model_dump_json())
    return clean_data
