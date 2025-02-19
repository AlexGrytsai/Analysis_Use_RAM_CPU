import json
import uuid
from typing import Any, Generator, Tuple

from redis import Redis


def get_test_data_from_json(
    file_path: str, num_of_objects: int
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
                obj["data"]["tenderID"] = key
                yield obj, key


def add_data_to_redis(
    redis_client: Redis,
    num_of_objects: int,
    file_path: str,
) -> None:
    for data, key in get_test_data_from_json(
        file_path=file_path, num_of_objects=num_of_objects
    ):
        redis_client.set(
            key, json.dumps(data, ensure_ascii=False)
        )
