from matplotlib import pyplot as plt


def make_graph_for_cpu(
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


def make_graph(mem_usage, interval, func_name):
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
