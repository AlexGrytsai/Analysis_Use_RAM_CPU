import json
from copy import deepcopy
from typing import Any, Generator


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
                yield deepcopy(obj)
