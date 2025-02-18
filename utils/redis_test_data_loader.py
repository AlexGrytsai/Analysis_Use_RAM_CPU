import json
import uuid
from typing import Any, Generator

from redis import Redis


def get_test_data_from_json(
    file_path: str, num_of_objects: int
) -> Generator[dict, Any, None]:
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)
        counter = 0
        while counter < num_of_objects:
            for obj in data:
                counter += 1
                if counter > num_of_objects:
                    break
                yield obj


def add_data_to_redis(
    redis_client: Redis,
    num_of_objects: int,
    file_path: str,
) -> None:
    for data in get_test_data_from_json(
        file_path=file_path, num_of_objects=num_of_objects
    ):
        redis_client.set(
            uuid.uuid4().hex, json.dumps(data, ensure_ascii=False)
        )
