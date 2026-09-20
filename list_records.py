import sys
import json
import redis

from src.argus.store import url_key


def get_records(url: str):
    try:
        r = redis.Redis(host="localhost", port=6379, db=1, decode_responses=True)

        records = r.hgetall(url_key(url))
        if not records:
            return f"URL '{url}' not found or empty."

        parsed_records = {}
        for identifier, record in records.items():
            parsed_records[identifier] = json.loads(record)

        return parsed_records
    except Exception as e:
        return f"Error connecting to Redis: {e}"


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python list_records.py '<url>'")
        print("Example: python list_records.py 'https://some-website.com/'")
        sys.exit(1)

    url = sys.argv[1]

    records = get_records(url)

    if isinstance(records, dict):
        print(json.dumps(records, indent=2))
    else:
        print(records)
