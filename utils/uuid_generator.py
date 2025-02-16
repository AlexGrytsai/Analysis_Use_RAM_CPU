import uuid
from typing import Generator, Any


def generate_uuids(num_of_ids: int) -> Generator[str, Any, None]:
    for _ in range(num_of_ids):
        yield uuid.uuid4().hex
