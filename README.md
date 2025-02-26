# Python Data Structures Performance Analysis

This repository contains code and benchmark results for various data structures
in Python. The goal of the study was to understand how Python manages memory
and how this affects performance when using different data types such as
`list`, `dict`, `set`, и `deque`.

## Sections

- [Research Objectives](#research-objectives)
- [Methodology](#methodology)
    - [Test data](#test-data)
    - [Data structures](#data-structures)
    - [Metrics](#metrics)
    - [Testing conditions](#еesting-conditions)
- [Results](#results)
    - [Graphs](#graphs)
        - [Generate IDs](#generate-ids)
        - [Membership](#membership)
        - [Create collactions with real data](#create-collactions-with-real-data)
        - [Clean raw data](#clean-raw-data)
        - [Various usage scenarios](#various-usage-scenarios)
        - [Adding data to the beginning of List and Deque](#adding-data-to-the-beginning-of-list-and-deque)
    - [Execution time](#execution-time)
    - [Optimization](#optimization)
- [Conclusions](#conclusions)

## Research Objectives

1. **Memory Management in Python**: How Python manages memory and how it
   affects performance.
2. **Comparison of data structures**: How Different Data Structures Affect
   Memory Usage, Execution Time, and CPU Load.
3. **Resource optimization**: How to optimize memory usage and execution time
   in real projects.

## Methodology

### Test data

- **UUID**: 100,000 unique identifiers (32-character UUIDs) were generated for
  testing..
- **Real data**: Data from the public API was used to test performance on more
  complex structures. 10,000 records were created.

### Data structures

- **List**
- **Dict**
- **Set**
- **Deque**

### Metrics

- **Memory (RAM)**: RAM usage.
- **Execution time**: Time spent on performing operations.
- **CPU Load**: CPU usage during execution.
- **Median value (50th percentile)**: This is the central value of the sample:
  half the data is smaller, half is larger. It shows the **typical** value
  well.
- **99th percentile**: This is the value below which 99% of the data falls.
  Shows the **worst cases**.

### Testing conditions

Each benchmark for each data structure was run 10 times manually via the
console.

## Results [⬆️](#sections)

### Graphs [⬆️](#sections)

#### Generate IDs [⬆️](#sections)

The code
is [here](https://github.com/AlexGrytsai/Analysis_Use_RAM_CPU/blob/main/benchmark/benchmark_create_simple_collections.py)
![Generate IDs (RAM)](https://github.com/AlexGrytsai/Analysis_Use_RAM_CPU/blob/main/images/generate_ids/ram_gener_collections_with_simple_data.png?raw=true)
![Generate IDs (CPU)](https://github.com/AlexGrytsai/Analysis_Use_RAM_CPU/blob/main/images/generate_ids/cpu_gener_collections_with_simple_data.png?raw=true)

#### Membership [⬆️](#sections)

The code
is [here](https://github.com/AlexGrytsai/Analysis_Use_RAM_CPU/blob/main/benchmark/benchmark_membership.py)
![Membership (RAM)](https://github.com/AlexGrytsai/Analysis_Use_RAM_CPU/blob/main/images/membership/ram_for_membership.png?raw=true)
![Membership (CPU)](https://github.com/AlexGrytsai/Analysis_Use_RAM_CPU/blob/main/images/membership/cpu_for_membership.png?raw=true)

#### Create collactions with real data [⬆️](#sections)

The code
is [here](https://github.com/AlexGrytsai/Analysis_Use_RAM_CPU/blob/main/benchmark/benchmark_create_collections_real_data.py)
![Collactions with real data (RAM)](https://github.com/AlexGrytsai/Analysis_Use_RAM_CPU/blob/main/images/add_data/ram_create_collections_with_real_data.png?raw=true)
![Collactions with real data (CPU)](https://github.com/AlexGrytsai/Analysis_Use_RAM_CPU/blob/main/images/add_data/cpu_create_collections_with_real_data.png?raw=true)

#### Clean raw data [⬆️](#sections)

The code
is [here](https://github.com/AlexGrytsai/Analysis_Use_RAM_CPU/blob/main/benchmark/benchmark_validate_data.py)
![Clean raw data (RAM)](https://github.com/AlexGrytsai/Analysis_Use_RAM_CPU/blob/main/images/validate/ram_validate_data.png?raw=true)
![Clean raw data (CPU)](https://github.com/AlexGrytsai/Analysis_Use_RAM_CPU/blob/main/images/validate/cpu_validate_data.png?raw=true)

#### Various usage scenarios [⬆️](#sections)

The code
is [here](https://github.com/AlexGrytsai/Analysis_Use_RAM_CPU/blob/main/benchmark_scenarios/scenario_use_min_ram.py)
![ram_diff_scenarios.png](https://github.com/AlexGrytsai/Analysis_Use_RAM_CPU/blob/main/images/scenario/ram_diff_scenarios.png?raw=true)
![enter image description here](https://github.com/AlexGrytsai/Analysis_Use_RAM_CPU/blob/main/images/scenario/cpu_diff_scenarios.png?raw=true)

#### Adding data to the beginning of List and Deque [⬆️](#sections)

The code
is [here](https://github.com/AlexGrytsai/Analysis_Use_RAM_CPU/blob/main/benchmark_scenarios/scenario_use_min_ram.py)
![enter image description here](https://github.com/AlexGrytsai/Analysis_Use_RAM_CPU/blob/main/images/scenario/ram_scenario_add_data_to_beginning_of_list_and_deque.png?raw=true)
![enter image description here](https://github.com/AlexGrytsai/Analysis_Use_RAM_CPU/blob/main/images/scenario/cpu_scenario_add_data_to_beginning_of_list_and_deque.png?raw=true)

### Execution time [⬆️](#sections)

- **List и Deque**: Showed similar results in terms of execution time.
- **Dict и Set**: Faster when searching for elements due to O(1) complexity.

### Optimization [⬆️](#sections)

**Scenario 5**: Most optimal in terms of memory usage.

```python
def scenario_v5(key_with_data: List[str], **kwargs) -> List[str]:
    all_ids_set = set(create_iterator_from_redis_keys())
    clean_data = []
    for id_data in set(key_with_data) & all_ids_set:
        clean_data.append(
            TenderDataValidator(
                **get_value_from_redis(key=id_data)
            ).model_dump_json()
        )
    return clean_data
```

**Scenario 5 Multiprocessing**: Most optimal in terms of memory usage and time
execution.

```python
def scenario_v5_multiprocessing(
    key_with_data: List[str], max_workers: int = None, **kwargs
) -> List[str]:
    all_ids_set = set(create_iterator_from_redis_keys())


membership_list = set(key_with_data) & all_ids_set

with ProcessPoolExecutor(max_workers=max_workers) as executor:
    clean_data = list(executor.map(process_tender_data, membership_list))

return clean_data
```

## Conclusions [⬆️](#sections)

- **List и Deque**: Lowest overhead for storing simple data.

- **Dict и Set**: Higher overhead, but faster when searching for elements. When
  storing container-type data, the overhead is no longer as significant.

- **Optimization**:
    - The creation of intermediate variables must be excluded..
    - Using `set` or `dict` to look up elements and minimize unnecessary data
      in memory.
    - Use multithreading when CPU-bound.

## License [⬆️](#sections)

This project is distributed under the MIT license.

## Contacts [⬆️](#sections)

If you have any questions or suggestions, please contact me
via [GitHub Issues](https://github.com/AlexGrytsai/Analysis_Use_RAM_CPU/issues)
or by email: [grytsai.alex@gmail.com](mailto:grytsai.alex@gmail.com).