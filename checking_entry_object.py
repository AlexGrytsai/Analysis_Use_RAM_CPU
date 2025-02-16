import uuid

from performance_monitoring.timer import timer_of_execution


@timer_of_execution
def check_entry_object_in_list(
    list_of_objects: list,
    number_of_checks: int,
) -> None:
    for _ in range(number_of_checks):
        entry_object: str = uuid.uuid4().hex
        if entry_object in list_of_objects:
            continue
        else:
            continue


@timer_of_execution
def check_entry_object_in_set(
    set_of_objects: set,
    number_of_checks: int,
) -> None:
    for _ in range(number_of_checks):
        entry_object: str = uuid.uuid4().hex
        if entry_object in set_of_objects:
            continue
        else:
            continue
