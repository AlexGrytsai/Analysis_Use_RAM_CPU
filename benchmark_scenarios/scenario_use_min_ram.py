from collections import deque
from concurrent.futures import ProcessPoolExecutor
from typing import List, Callable, Type

from pympler import asizeof

from performance_monitoring.cpu import cpu_monitor_decorator
from performance_monitoring.ram import ram_monitor_decorator
from utils.redis_for_save_usage_data import usage_r_client
from utils.redis_test_data_loader import (
    create_iterator_from_redis_keys,
    get_value_from_redis,
    get_list_keys_with_data,
)
from utils.validators import TenderDataValidator


@cpu_monitor_decorator(r_client=usage_r_client)
@ram_monitor_decorator(r_client=usage_r_client)
def scenario_v1(
    key_with_data: List[str], **kwargs
) -> list[TenderDataValidator]:
    all_ids_list = []
    redis_iterator = create_iterator_from_redis_keys()
    for id_ in redis_iterator:
        all_ids_list.append(id_)

    all_ids_set = set(all_ids_list)
    membership_list = []

    for id_data in all_ids_set:
        if id_data in set(key_with_data):
            membership_list.append(id_data)

    raw_data_list = []

    for id_data in membership_list:
        data_from_redis = get_value_from_redis(key=id_data)
        raw_data_list.append(data_from_redis)

    clean_data = []

    for data in raw_data_list:
        validate_date = TenderDataValidator(**data)
        clean_data.append(validate_date)

    return clean_data


@cpu_monitor_decorator(r_client=usage_r_client)
@ram_monitor_decorator(r_client=usage_r_client)
def scenario_v2(
    key_with_data: List[str], **kwargs
) -> list[TenderDataValidator]:
    all_ids_list = [id_ for id_ in create_iterator_from_redis_keys()]

    all_ids_set = set(all_ids_list)
    membership_list = set(key_with_data) & all_ids_set

    raw_data_list = [
        get_value_from_redis(key=id_data) for id_data in membership_list
    ]

    clean_data = [TenderDataValidator(**data) for data in raw_data_list]

    return clean_data


@cpu_monitor_decorator(r_client=usage_r_client)
@ram_monitor_decorator(r_client=usage_r_client)
def scenario_v3(
    key_with_data: List[str], **kwargs
) -> list[TenderDataValidator]:
    membership_list = []

    for id_ in create_iterator_from_redis_keys():
        if id_ in key_with_data:
            membership_list.append(id_)

    clean_data = []
    for id_data in membership_list:
        clean_data.append(
            TenderDataValidator(**get_value_from_redis(key=id_data))
        )

    return clean_data


@cpu_monitor_decorator(r_client=usage_r_client)
@ram_monitor_decorator(r_client=usage_r_client)
def scenario_v4(
    key_with_data: List[str], **kwargs
) -> list[TenderDataValidator]:
    all_ids_set = set(create_iterator_from_redis_keys())

    membership_list = set(key_with_data) & all_ids_set

    clean_data = []
    for id_data in membership_list:
        clean_data.append(
            TenderDataValidator(**get_value_from_redis(key=id_data))
        )

    return clean_data


def process_tender_data(id_data: str) -> str:
    return TenderDataValidator(
        **get_value_from_redis(key=id_data)
    ).model_dump_json()


@cpu_monitor_decorator(r_client=usage_r_client)
@ram_monitor_decorator(r_client=usage_r_client)
def scenario_v5(key_with_data: List[str], **kwargs) -> List[str]:
    all_ids_set = set(create_iterator_from_redis_keys())

    membership_list = set(key_with_data) & all_ids_set

    clean_data = []
    for id_data in membership_list:
        clean_data.append(process_tender_data(id_data))

    return clean_data


@cpu_monitor_decorator(r_client=usage_r_client)
@ram_monitor_decorator(r_client=usage_r_client)
def scenario_v5_multiprocessing(
    key_with_data: List[str], max_workers: int = None, **kwargs
) -> List[str]:
    all_ids_set = set(create_iterator_from_redis_keys())
    membership_list = set(key_with_data) & all_ids_set

    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        clean_data = list(executor.map(process_tender_data, membership_list))

    return clean_data


@cpu_monitor_decorator(r_client=usage_r_client)
@ram_monitor_decorator(r_client=usage_r_client)
def scenario_v6(key_with_data: List[str], **kwargs) -> None:
    all_ids_set = set(create_iterator_from_redis_keys())

    membership_list = set(key_with_data) & all_ids_set

    for id_data in membership_list:
        usage_r_client.set(
            id_data,
            TenderDataValidator(
                **get_value_from_redis(key=id_data)
            ).model_dump_json(),
        )


@cpu_monitor_decorator(r_client=usage_r_client)
@ram_monitor_decorator(r_client=usage_r_client)
def scenario_v7(**kwargs) -> List[str]:
    raw_data_list = []

    for id_ in create_iterator_from_redis_keys():
        raw_data_list.insert(0, id_)

    return raw_data_list


@cpu_monitor_decorator(r_client=usage_r_client)
@ram_monitor_decorator(r_client=usage_r_client)
def scenario_v8(**kwargs) -> deque[List[str]]:
    raw_data_list = deque([])

    for id_ in create_iterator_from_redis_keys():
        raw_data_list.appendleft(id_)

    return raw_data_list


def run_benchmark_scenarios(
    scenario: Type[Callable],
    is_print_size: bool = False,
) -> None:
    ids_with_data = get_list_keys_with_data()

    data_for_benchmark = {
        scenario_v1: "Scenario #1",
        scenario_v2: "Scenario #2",
        scenario_v3: "Scenario #3",
        scenario_v4: "Scenario #4",
        scenario_v5: "Scenario #5",
        scenario_v5_multiprocessing: "Scenario #5 Multiprocessing",
        scenario_v6: "Scenario #6",
        scenario_v7: "Adding data to the beginning of the list",
        scenario_v8: "Adding data to the beginning of the deque",
    }

    data_from_scenario = scenario(
        key_with_data=ids_with_data, func_name=data_for_benchmark[scenario]
    )

    if is_print_size:
        print(
            f"Size of {data_for_benchmark[scenario]}: "
            f"{asizeof.asizeof(data_from_scenario) / 1024 / 1024:.2f} MB"
        )


if __name__ == "__main__":
    run_benchmark_scenarios(scenario=scenario_v1, is_print_size=True)
