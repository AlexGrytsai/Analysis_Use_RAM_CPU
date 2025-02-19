import json
import uuid
from typing import Any, Generator, Tuple, List

from redis import Redis


def change_object_id_in_test_data(obj: dict, new_id: str) -> dict:
    obj["data"]["tenderID"] = new_id
    return obj


def get_test_data_from_json(
    file_path: str,
    num_of_objects: int,
) -> Generator[Tuple[Any, str], Any, None]:
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)
        counter = 0
        while counter < num_of_objects:
            for obj in data:
                counter += 1
                if counter > num_of_objects:
                    break
                key = uuid.uuid4().hex
                yield change_object_id_in_test_data(obj, key), key


def generate_uuid_keys_for_redis(
    num_of_keys: int,
) -> Generator[str, Any, None]:
    for _ in range(num_of_keys):
        yield uuid.uuid4().hex


def add_data_to_redis(
    redis_client: Redis,
    num_of_objects: int,
    file_path: str,
) -> List[str]:
    list_key_with_data = []
    for data, key in get_test_data_from_json(
        file_path=file_path, num_of_objects=num_of_objects
    ):
        redis_client.set(key, json.dumps(data, ensure_ascii=False))
        list_key_with_data.append(key)
    return list_key_with_data


def add_empty_keys_to_redis(redis_client: Redis, num_of_keys: int) -> None:
    for key in generate_uuid_keys_for_redis(num_of_keys=num_of_keys):
        redis_client.set(key, "")


def prepare_data_for_benchmark(
    redis_client: Redis,
    total_keys: int,
    num_keys_with_data: int,
    file_path: str,
) -> List[str]:
    add_empty_keys_to_redis(
        redis_client=redis_client, num_of_keys=total_keys - num_keys_with_data
    )
    return add_data_to_redis(
        redis_client=redis_client,
        num_of_objects=num_keys_with_data,
        file_path=file_path,
    )
