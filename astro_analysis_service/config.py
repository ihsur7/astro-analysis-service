"""Application configuration helpers."""
from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


DEFAULT_CACHE_PATH = Path(__file__).resolve().parent / "data" / "cache" / "nasa_exoplanets.json"


@dataclass(slots=True)
class Settings:
    """Simple settings container sourced from environment variables."""

    nasa_cache_ttl_seconds: int = int(os.getenv("NASA_CACHE_TTL_SECONDS", "86400"))
    nasa_max_records: int = int(os.getenv("NASA_MAX_RECORDS", "150"))
    nasa_cache_path: Path = Path(os.getenv("NASA_CACHE_PATH", str(DEFAULT_CACHE_PATH)))


settings = Settings()
settings.nasa_cache_path.parent.mkdir(parents=True, exist_ok=True)
