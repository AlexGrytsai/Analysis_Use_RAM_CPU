from get_ids import (
    generate_ids_in_list,
    generate_ids_in_set,
    generate_ids_in_deque,
    generate_ids_in_dict,
)
from performance_monitoring.cpu import cpu_monitor_decorator
from performance_monitoring.memory import memory_object_report
from performance_monitoring.ram import ram_monitor_decorator


def analyze_performance_generation_list_with_ids(
    num_ids: int,
) -> None:
    ids_list = ram_monitor_decorator(is_detail=True)(
        cpu_monitor_decorator(generate_ids_in_list)
    )(num_ids)
    memory_object_report(ids_list)

    ids_deque = ram_monitor_decorator(is_detail=True)(
        cpu_monitor_decorator(generate_ids_in_deque)
    )(num_ids)
    memory_object_report(ids_deque)

    ids_set = ram_monitor_decorator(is_detail=True)(
        cpu_monitor_decorator(generate_ids_in_set)
    )(num_ids)
    memory_object_report(ids_set)

    ids_dict = ram_monitor_decorator(is_detail=True)(
        cpu_monitor_decorator(generate_ids_in_dict)
    )(num_ids)
    memory_object_report(ids_dict)
