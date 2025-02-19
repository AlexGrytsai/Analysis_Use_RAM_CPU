from collections import deque
from time import sleep
from typing import List, Any, Dict, Set

from performance_monitoring.cpu import cpu_monitor_decorator, cpu_usage_results
from performance_monitoring.memory import memory_object_report
from performance_monitoring.ram import ram_monitor_decorator, ram_usage_results
from utils.graphs import plot_combined_graph_for_cpu, plot_combined_ram_graph
from utils.redis_test_data_loader import fetch_data_from_redis_for_structure


@ram_monitor_decorator()
@cpu_monitor_decorator()
def load_list_from_redis(
    key_list: List[str],
    **kwargs,
) -> List[dict[str, Any]]:
    return fetch_data_from_redis_for_structure(
        key_list=key_list, data_structure=list
    )


@ram_monitor_decorator()
@cpu_monitor_decorator()
def load_deque_from_redis(
    key_list: List[str],
    **kwargs,
) -> deque[Dict[str, Any]]:
    return fetch_data_from_redis_for_structure(
        key_list=key_list, data_structure=deque
    )


@ram_monitor_decorator()
@cpu_monitor_decorator()
def load_dict_from_redis(
    key_list: List[str],
    **kwargs,
) -> Dict[str, Any]:
    return fetch_data_from_redis_for_structure(
        key_list=key_list, data_structure=dict
    )


@ram_monitor_decorator()
@cpu_monitor_decorator()
def load_set_from_redis(
    key_list: List[str],
    **kwargs,
) -> Set[bytes]:
    return fetch_data_from_redis_for_structure(
        key_list=key_list, data_structure=set
    )


def benchmark_data_structures(
    redis_keys: List[str],
    memory_report: bool = False,
) -> None:
    data_structures = {
        "List": load_list_from_redis,
        "Deque": load_deque_from_redis,
        "Dict": load_dict_from_redis,
        "Set": load_set_from_redis,
    }

    loaded_data = {}
    for name, func in data_structures.items():
        loaded_data[name] = func(
            key_list=redis_keys,
            func_name=f"Load data to {name}",
        )
        sleep(1)

    if memory_report:
        for _, data in loaded_data.items():
            memory_object_report(data)


def main_benchmark_add_data(
    list_keys: List[str],
    repeat: int = 10,
) -> None:
    for _ in range(repeat):
        benchmark_data_structures(
            redis_keys=list_keys,
            memory_report=True,
        )

    plot_combined_graph_for_cpu(cpu_data=cpu_usage_results)
    plot_combined_ram_graph(ram_data=ram_usage_results)
