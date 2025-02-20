from typing import Dict, List

import numpy as np
from matplotlib import pyplot as plt


def plot_individual_graph_for_cpu(
    cpu_usage: List[float],
    func_name: str,
    exec_time: float,
) -> None:
    avg_cpu = sum(cpu_usage) / len(cpu_usage) if cpu_usage else 0
    max_cpu = max(cpu_usage, default=0)

    plt.figure(figsize=(10, 6))
    time_points = [i * 0.1 for i in range(len(cpu_usage))]

    plt.plot(
        time_points,
        cpu_usage,
        marker="o",
        color="r",
        label="CPU Usage (%)",
    )

    plt.ylim(0, 50)

    plt.title(f"CPU Usage for Function: {func_name}")
    plt.xlabel("Time (seconds)")
    plt.ylabel("CPU Usage (%)")
    plt.ylim(0, 50)
    plt.grid(True)
    plt.legend(loc="center", bbox_to_anchor=(0.5, -0.3))
    plt.subplots_adjust(bottom=0.3)

    text_x = time_points[-1] * 0.7
    text_y = 40
    plt.text(
        text_x,
        text_y,
        f"Exec Time: {exec_time:.2f}s\n"
        f"Avg CPU: {avg_cpu:.2f}%\n"
        f"Peak CPU: {max_cpu:.2f}%",
        fontsize=10,
        bbox=dict(facecolor="white", alpha=0.8, edgecolor="gray"),
    )

    plt.show()


def plot_combined_graph_for_cpu(
    cpu_data: Dict[str, List[List[float]]],
) -> None:
    plt.figure(figsize=(10, 6))

    for func_name, runs in cpu_data.items():
        if not runs:
            continue

        median_runs = [np.median(run) for run in runs]
        max_length = max(map(len, runs), default=0)

        if max_length == 0:
            continue

        avg_cpu_usage = [
            np.mean([run[i] for run in runs if i < len(run)])
            for i in range(max_length)
        ]

        exec_time = max_length * 0.1
        max_cpu = np.max(avg_cpu_usage) if avg_cpu_usage else 0

        plt.plot(
            [i * 0.1 for i in range(len(avg_cpu_usage))],
            avg_cpu_usage,
            marker="o",
            label=(
                f"{func_name} (Exec Time: {exec_time:.2f}s, "
                f"Median: {np.median(median_runs):.2f}%, Peak: {max_cpu:.2f}%)"
            ),
        )

    plt.title("CPU Usage Comparison")
    plt.xlabel("Time (seconds)")
    plt.ylabel("CPU Usage (%)")
    plt.ylim(0, 100)
    plt.yticks(np.linspace(0, 100, 10))
    plt.grid(True)
    plt.legend(loc="center", bbox_to_anchor=(0.5, -0.3))
    plt.subplots_adjust(bottom=0.3)
    plt.show()


def plot_individual_ram_graph(mem_usage, interval, func_name):
    plt.figure(figsize=(10, 6))
    plt.plot(
        [i * interval for i in range(len(mem_usage))],
        mem_usage,
        marker="o",
        color="b",
        label="RAM Usage (MB)",
    )
    plt.title(f"RAM Usage for Function: {func_name}")
    plt.xlabel("Time (seconds)")
    plt.ylabel("RAM Usage (MB)")
    plt.grid(True)
    plt.legend(loc="center", bbox_to_anchor=(0.5, -0.3))
    plt.subplots_adjust(bottom=0.3)
    plt.show()


def plot_combined_ram_graph(
    ram_data: Dict[str, List[List[float]]],
    y_limit: int = None,
    detailing: int = None,
) -> None:
    plt.figure(figsize=(10, 6))

    y_limit = y_limit or 1.1 * max(
        max(max(run, default=0) for run in data) if data else 0
        for data in ram_data.values()
    )
    detailing = detailing or 10

    for func_name, runs in ram_data.items():
        avg_runs = [np.mean(run) for run in runs]
        max_length = max(map(len, runs), default=0)
        median_runs = [np.median(run) for run in runs]
        avg_ram_usage = [
            np.mean([run[i] for run in runs if i < len(run)])
            for i in range(max_length)
        ]

        plt.plot(
            [i * 0.1 for i in range(len(avg_ram_usage))],
            avg_ram_usage,
            marker="o",
            label=(
                f"{func_name} (Avg Peak: {np.mean(avg_runs):.2f} MB, "
                f"Median: {np.mean(median_runs):.2f} MB)"
            ),
        )

    plt.title("RAM Usage Comparison")
    plt.xlabel("Time (seconds)")
    plt.ylabel("RAM Usage (MB)")
    plt.ylim(0, y_limit)
    plt.yticks(np.linspace(0, y_limit, detailing))
    plt.grid(True)
    plt.legend(loc="center", bbox_to_anchor=(0.5, -0.3))
    plt.subplots_adjust(bottom=0.3)
    plt.show()
