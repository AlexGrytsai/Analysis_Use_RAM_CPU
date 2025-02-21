from benchmark.benchmark_create_collections import (
    main_benchmark_ids_generation,
)
from benchmark.benchmark_data_structures import (
    main_benchmark_add_data,
)
from benchmark.benchmark_membership import (
    main_benchmark_membership,
)
from benchmark.benchmark_validate_data import main_benchmark_validate_data
from utils.redis_test_data_loader import (
    prepare_data_for_benchmark,
    clean_redis_database,
)


def main(
    command: str,
    num_ids: int = 100_000,
    num_ids_with_data: int = 5_000,
) -> None:
    list_keys_with_data = prepare_data_for_benchmark(
        file_path="test_data.json",
        total_keys=num_ids,
        num_keys_with_data=num_ids_with_data,
    )
    match command:
        case "gener":
            main_benchmark_ids_generation()
        case "mem":
            main_benchmark_membership(list_keys=list_keys_with_data)
        case "add":
            main_benchmark_add_data(list_keys=list_keys_with_data)
        case "val":
            main_benchmark_validate_data(list_keys=list_keys_with_data)

    clean_redis_database()


if __name__ == "__main__":
    comm = input("Enter a command (gener, mem, add, val): ").strip()
    if not comm:
        print("Command is required!")
    else:
        try:
            ids = input(
                "Enter the number of ids (press Enter for default): "
            ).strip()
            ids = int(ids) if ids else 100_000

            ids_with_data = input(
                "Enter the number of ids with data (press Enter for default): "
            ).strip()
            ids_with_data = int(ids_with_data) if ids_with_data else 5_000

            main(comm, ids, ids_with_data)
        except ValueError:
            print("Invalid input. Please enter a valid number.")
