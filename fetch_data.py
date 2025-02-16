from typing import List, Any

from performance_monitoring.timer import timer_of_execution
from utils.get_test_data import get_test_data_from_json


@timer_of_execution
def fetch_test_data_in_list(file_path: str) -> List[dict[str, Any]]:
    data_list = []
    for data in get_test_data_from_json(file_path):
        data_list.append(data)
    return data_list
