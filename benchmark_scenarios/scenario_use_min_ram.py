from typing import List

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
def scenario_use_min_ram_sequence_not_important_v1(
    key_with_data: List[str],
) -> list[TenderDataValidator]:
    all_ids_list = []
    redis_iterator = create_iterator_from_redis_keys()
    for id_ in redis_iterator:
        all_ids_list.append(id_)

    all_ids_set = set(all_ids_list)
    membership_list = []

    for id_data in key_with_data:
        if id_data in all_ids_set:
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


if __name__ == "__main__":
    scenario_use_min_ram_sequence_not_important_v1(get_list_keys_with_data())
