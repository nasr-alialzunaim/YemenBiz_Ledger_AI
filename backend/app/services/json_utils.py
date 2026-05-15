import json
import re


def safe_json_loads(value: str, default):
    try:
        return json.loads(value)
    except Exception:
        return default


def extract_json_object(text: str) -> dict:
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if not match:
        return {}
    return safe_json_loads(match.group(0), {})
