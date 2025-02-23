import json
from typing import Dict, List, Tuple

import redis
from redis import Redis

usage_r_client = redis.Redis(
    host="localhost",
    port=6379,
    db=4,
    decode_responses=True,
)


def load_all_ram_usage_from_redis(
    key_prefix: str,
    r_client: Redis = usage_r_client,
) -> Dict[str, List[Tuple[List[float], float]]] | None:
    ram_usage_results = {}

    try:
        keys = r_client.keys(f"{key_prefix}*")
        if not keys:
            print("Redis does not contain any data")

        for key in keys:
            value = r_client.lrange(key, 0, -1)
            clean_key = key.replace(key_prefix, "")
            if clean_key not in ram_usage_results:
                ram_usage_results[clean_key] = []
            for item in value:
                ram_usage_results[clean_key].append(
                    (json.loads(item)[0], json.loads(item)[1])
                )

        return ram_usage_results

    except Exception as exc:
        raise Exception(f"Error loading data from Redis: {exc}")
