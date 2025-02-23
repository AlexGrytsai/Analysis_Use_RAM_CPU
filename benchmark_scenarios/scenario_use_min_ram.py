from typing import List

from performance_monitoring.cpu import cpu_monitor_decorator
from performance_monitoring.ram import ram_monitor_decorator
from utils.redis_for_save_usage_data import usage_r_client
from utils.redis_test_data_loader import (
    create_iterator_from_redis_keys,
    get_value_from_redis,
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


@cpu_monitor_decorator(r_client=usage_r_client)
@ram_monitor_decorator(r_client=usage_r_client)
def scenario_v5(key_with_data: List[str], **kwargs) -> List[str]:
    all_ids_set = set(create_iterator_from_redis_keys())

    membership_list = set(key_with_data) & all_ids_set

    clean_data = []
    for id_data in membership_list:
        clean_data.append(
            TenderDataValidator(
                **get_value_from_redis(key=id_data)
            ).model_dump_json()
        )

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
