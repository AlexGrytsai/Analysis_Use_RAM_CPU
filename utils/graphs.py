from matplotlib import pyplot as plt


def plot_individual_graph_for_cpu(
    cpu_usage: list,
    func_name: str,
    exec_time: float,
    avg_cpu: float,
    max_cpu: float,
) -> None:
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
    plt.grid(True)
    plt.legend()

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


def plot_combined_graph_for_cpu(cpu_data: dict) -> None:
    plt.figure(figsize=(10, 6))

    for func_name, data in cpu_data.items():
        exec_time, avg_cpu, max_cpu, cpu_usage = data

        plt.plot(
            [i * 0.1 for i in range(len(cpu_usage))],
            cpu_usage,
            marker="o",
            label=f"{func_name} (Exec Time: {exec_time:.2f}s, Avg CPU: {avg_cpu:.2f}%, Peak CPU: {max_cpu:.2f}%)",
        )

    plt.title("CPU Usage Comparison")
    plt.xlabel("Time (seconds)")
    plt.ylabel("CPU Usage (%)")
    plt.ylim(0, 50)
    plt.grid(True)
    plt.legend()
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
    plt.legend()
    plt.show()


def plot_combined_ram_graph(ram_data: dict) -> None:
    plt.figure(figsize=(10, 6))

    for func_name, data in ram_data.items():
        max_ram, ram_usage, interval = data
        plt.plot(
            [i * interval for i in range(len(ram_usage))],
            ram_usage,
            marker="o",
            label=f"{func_name} (Peak RAM: {max_ram:.2f} MB)",
        )

    plt.title("RAM Usage Comparison")
    plt.xlabel("Time (seconds)")
    plt.ylabel("RAM Usage (MB)")
    plt.grid(True)
    plt.legend()
    plt.show()
