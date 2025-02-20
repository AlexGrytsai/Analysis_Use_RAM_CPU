import numpy as np
import matplotlib.pyplot as plt
from typing import Dict, List, Tuple


def plot_resource_usage(
    resource_data: Dict[str, List[Tuple[List[float], float]]],
    title: str,
    y_label: str,
    y_limit: int = None,
    detailing: int = 10,
    is_cpu: bool = False,
) -> None:
    plt.figure(figsize=(10, 6))

    y_limit = y_limit or (
        100
        if is_cpu
        else 1.1
             * max(
            max(max(run[0], default=0) for run in data) if data else 0
            for data in resource_data.values()
        )
    )

    for func_name, runs in resource_data.items():
        if not runs:
            continue

        all_resource_usages = [run[0] for run in runs]
        exec_times = [run[1] for run in runs]

        max_length = max(map(len, all_resource_usages), default=0)
        if max_length == 0:
            continue

        avg_resource_usage = [
            np.mean([run[i] for run in all_resource_usages if i < len(run)])
            for i in range(max_length)
        ]

        avg_exec_time = np.mean(exec_times)
        x_values = np.linspace(0, avg_exec_time, len(avg_resource_usage))

        median_resource = np.median(
            [np.median(run) for run in all_resource_usages]
        )
        max_resource = np.max(avg_resource_usage) if avg_resource_usage else 0

        plt.plot(
            x_values,
            avg_resource_usage,
            marker="o",
            label=(
                f"{func_name} (Exec Time: {avg_exec_time:.2f}s, "
                f"Median: {median_resource:.2f}{'%' if is_cpu else ' MB'}, "
                f"Peak: {max_resource:.2f}{'%' if is_cpu else ' MB'})"
            ),
        )

    plt.title(title)
    plt.xlabel("Time (seconds)")
    plt.ylabel(y_label)
    plt.ylim(0, y_limit)
    plt.yticks(np.linspace(0, y_limit, detailing))
    plt.grid(True)
    plt.legend(loc="center", bbox_to_anchor=(0.5, -0.3))
    plt.subplots_adjust(bottom=0.3)
    plt.show()


def plot_combined_ram_graph(
    ram_data: Dict[str, List[Tuple[List[float], float]]],
    y_limit: int = None,
    detailing: int = None,
) -> None:
    plot_resource_usage(
        ram_data,
        title="RAM Usage Comparison",
        y_label="RAM Usage (MB)",
        y_limit=y_limit,
        detailing=detailing or 10,
        is_cpu=False,
    )


def plot_combined_graph_for_cpu(
    cpu_data: Dict[str, List[Tuple[List[float], float]]],
) -> None:
    plot_resource_usage(
        cpu_data,
        title="CPU Usage Comparison",
        y_label="CPU Usage (%)",
        y_limit=100,
        detailing=20,
        is_cpu=True,
    )
