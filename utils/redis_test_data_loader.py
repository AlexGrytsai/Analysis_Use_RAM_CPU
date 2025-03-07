import json
import uuid
from collections import deque
from typing import (
    Any,
    Generator,
    Tuple,
    List,
    Iterator,
    Type,
    Union,
    Dict,
    Set,
)

import redis
from redis import Redis

r_client_prepare = redis.Redis(
    host="localhost",
    port=6379,
    db=3,
    decode_responses=True,
)


def change_object_id_in_test_data(obj: dict, new_id: str) -> dict:
    obj["data"]["tenderID"] = new_id
    return obj


def create_iterator_from_redis_keys(
    r_client: Redis = r_client_prepare,
) -> Iterator[str]:
    return r_client.scan_iter("*")


def get_value_from_redis(
    key: str,
    r_client: Redis = r_client_prepare,
) -> Dict[str, Any]:
    return json.loads(r_client.get(key))


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


def clean_redis_database(r_client: Redis = r_client_prepare) -> None:
    r_client.flushdb()


def add_data_to_redis(
    num_of_objects: int,
    file_path: str,
    r_client: Redis = r_client_prepare,
) -> List[str]:
    list_key_with_data = []
    for data, key in get_test_data_from_json(
        file_path=file_path, num_of_objects=num_of_objects
    ):
        r_client.set(key, json.dumps(data, ensure_ascii=False))
        list_key_with_data.append(key)
    return list_key_with_data


def add_empty_keys_to_redis(
    num_of_keys: int,
    r_client: Redis = r_client_prepare,
) -> None:
    for key in generate_uuid_keys_for_redis(num_of_keys=num_of_keys):
        r_client.set(key, "")


def get_list_keys_with_data(r_client: Redis = r_client_prepare) -> List[str]:
    return r_client.lrange("list_keys_with_data", 0, -1)


def fetch_data_from_redis_for_structure(
    data_structure: Type[Union[list, deque, dict, set]],
    r_client: Redis = r_client_prepare,
    **kwargs,
) -> Union[
    List[dict[str, Any]], deque[Dict[str, Any]], Dict[str, Any], Set[bytes]
]:
    ids_list_with_data = get_list_keys_with_data()
    if data_structure is list:
        return [json.loads(r_client.get(key)) for key in ids_list_with_data]

    elif data_structure is deque:
        return deque(
            json.loads(r_client.get(key)) for key in ids_list_with_data
        )

    elif data_structure is set:
        return {r_client.get(key) for key in ids_list_with_data}

    elif data_structure is dict:
        return {
            uuid.uuid4().hex: json.loads(r_client.get(key))
            for key in ids_list_with_data
        }

    raise ValueError(f"Unsupported data structure: {data_structure}")


def prepare_data_for_benchmark(
    total_keys: int,
    num_keys_with_data: int,
    file_path: str,
    r_client: Redis = r_client_prepare,
) -> List[str]:
    add_empty_keys_to_redis(
        r_client=r_client, num_of_keys=total_keys - num_keys_with_data
    )
    return add_data_to_redis(
        r_client=r_client,
        num_of_objects=num_keys_with_data,
        file_path=file_path,
    )


if __name__ == "__main__":
    num_ids = 100_000
    num_ids_with_data = 10_000

    clean_redis_database()

    list_ids_with_data = prepare_data_for_benchmark(
        file_path="../test_data.json",
        total_keys=num_ids,
        num_keys_with_data=num_ids_with_data,
    )

    r_client_prepare.rpush("list_keys_with_data", *list_ids_with_data)
