from get_ids import (
    generate_ids_in_list,
    generate_ids_in_set,
    generate_ids_in_deque,
    generate_ids_in_dict,
)
from performance_monitoring.memory import memory_object_report
from performance_monitoring.timer import timer_of_execution


def analyze_performance_generation_list_with_ids(
    num_ids: int,
) -> None:
    ids_list = timer_of_execution(generate_ids_in_list)(num_ids)
    ids_deque = timer_of_execution(generate_ids_in_deque)(num_ids)
    ids_set = timer_of_execution(generate_ids_in_set)(num_ids)
    ids_dict = timer_of_execution(generate_ids_in_dict)(num_ids)

    memory_object_report(ids_list)
    memory_object_report(ids_deque)
    memory_object_report(ids_set)
    memory_object_report(ids_dict)
