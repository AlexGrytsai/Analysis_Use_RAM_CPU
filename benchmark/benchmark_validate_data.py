from collections import deque
from typing import List, Any, Dict

from utils.validators import TenderDataValidator


def validate_data_from_list(
    raw_data_list: List[Dict[str, Any]],
) -> List[TenderDataValidator]:
    clean_data = []
    for data in raw_data_list:
        validate_date = TenderDataValidator(**data)
        clean_data.append(validate_date)
    return clean_data


def validate_data_from_deque(
    raw_data_deque: deque,
) -> deque[TenderDataValidator]:
    clean_data = deque([])
    for data in raw_data_deque:
        validate_date = TenderDataValidator(**data)
        clean_data.append(validate_date)
    return clean_data


def validate_data_from_dict(
    raw_data_dict: Dict[str, Any],
) -> Dict[str, TenderDataValidator]:
    clean_data = {}
    for key, value in raw_data_dict.items():
        validate_date = TenderDataValidator(**value)
        clean_data[key] = validate_date
    return clean_data
