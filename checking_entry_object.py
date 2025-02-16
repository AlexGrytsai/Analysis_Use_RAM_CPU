import uuid

from performance_monitoring.timer import timer_of_execution


@timer_of_execution
def check_entry_object_in_list(
    list_of_objects: list,
    entry_object: str = uuid.uuid4().hex,
) -> bool:
    return entry_object in list_of_objects


@timer_of_execution
def check_entry_object_in_set(
    set_of_objects: set,
    entry_object: str = uuid.uuid4().hex,
) -> bool:
    return entry_object in set_of_objects
