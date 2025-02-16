import json
from typing import Any, Generator


def get_test_data_from_json(file_path: str) -> Generator[dict, Any, None]:
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)
        for obj in data:
            yield obj
