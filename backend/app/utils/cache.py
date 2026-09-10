"""Simple in-memory TTL cache."""
import time
from typing import Any

_store: dict[str, tuple[Any, float]] = {}


def get(key: str) -> Any | None:
    if key in _store:
        val, exp = _store[key]
        if time.time() < exp:
            return val
        del _store[key]
    return None


def set(key: str, value: Any, ttl: int = 180) -> None:
    _store[key] = (value, time.time() + ttl)
