import json
from typing import List


def open_json_file(file_path: str) -> List[dict]:
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)
    return data


def write_json_file(file_path: str, data: List[dict]) -> None:
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)
