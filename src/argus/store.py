import hashlib
import json
import logging

from typing import List

import redis.asyncio as redis

def url_key(url: str):
    url_slug = hashlib.md5(url.encode()).hexdigest()
    return f"url:{url_slug}"


async def upsert(url: str, extracted: List) -> bool:
    if not extracted:
        logging.info(f"Nothing extracted for {url}")
        return False

    redis_key = url_key(url)
    redis_client = redis.Redis.from_url(
        "redis://localhost:6379/1",
        decode_responses=True,
    )

    try:
        record_mapping = {}
        for record in extracted:
            identifier = record.get("id")
            if identifier:
                record_mapping[str(identifier)] = json.dumps(record)

        if not record_mapping:
            logging.info(f"No records to upsert for {url}")
            return False

        existing_records = await redis_client.hgetall(redis_key)
        changed = set(existing_records.keys()) != set(record_mapping.keys())
        stale_ids = set(existing_records.keys()) - set(record_mapping.keys())

        async with redis_client.pipeline(transaction=True) as pipe:
            pipe.hset(redis_key, mapping=record_mapping)
            if stale_ids:
                pipe.hdel(redis_key, *stale_ids)
            await pipe.execute()

        if changed:
            logging.info(f"Updated {len(record_mapping)} records for {url}")
        else:
            logging.info(f"No record IDs changed for {url}")

        return changed
    finally:
        await redis_client.aclose()
