import json
from collections import deque
from typing import List, Any, Dict, Set, Union, Type

from pympler import asizeof

from performance_monitoring.cpu import cpu_monitor_decorator
from performance_monitoring.ram import ram_monitor_decorator
from utils.redis_for_save_usage_data import usage_r_client
from utils.redis_test_data_loader import fetch_data_from_redis_for_structure
from utils.validators import TenderDataValidator

CLEANED_DATA_TYPE = (
    Union[
        List[TenderDataValidator],
        deque[TenderDataValidator],
        Dict[str, TenderDataValidator],
        Set[str],
    ],
)


def validate(item: Dict[str, Any]) -> TenderDataValidator:
    return TenderDataValidator(**item)


@cpu_monitor_decorator(r_client=usage_r_client)
@ram_monitor_decorator(r_client=usage_r_client)
def benchmark_validate_data(
    raw_data: Union[List, deque, Dict, Set[str]],
    **kwargs,
) -> CLEANED_DATA_TYPE:
    if isinstance(raw_data, list):
        return [validate(data) for data in raw_data]

    elif isinstance(raw_data, deque):
        return deque(validate(data) for data in raw_data)

    elif isinstance(raw_data, dict):
        return {key: validate(value) for key, value in raw_data.items()}

    elif isinstance(raw_data, set):
        return {
            validate(json.loads(value)).model_dump_json() for value in raw_data
        }

    else:
        raise ValueError(f"Unsupported data structure: {type(raw_data)}")


def run_benchmark_validate_data(
    type_collection: Type[Union[list, deque, dict, set]],
    is_print_size: bool = False,
) -> None:
    data_for_benchmark = {
        list: "Create List with clean data",
        deque: "Create Deque with clean data",
        set: "Create Set with clean data",
        dict: "Create Dict with clean data",
    }

    clean_data = benchmark_validate_data(
        raw_data=fetch_data_from_redis_for_structure(
            data_structure=type_collection
        ),
        func_name=data_for_benchmark[type_collection],
    )

    if is_print_size:
        print(
            f"Size of {data_for_benchmark[type_collection]}: "
            f"{asizeof.asizeof(clean_data) / 1024 / 1024:.2f} MB"
        )


if __name__ == "__main__":
    run_benchmark_validate_data(type_collection=set, is_print_size=True)
