"""Client for retrieving data from the NASA Exoplanet Archive."""
from __future__ import annotations

import json
import logging
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Iterable, List, Sequence

import httpx

from .config import settings

LOGGER = logging.getLogger(__name__)

EXOPLANET_ENDPOINT = "https://exoplanetarchive.ipac.caltech.edu/TAP/sync"
QUERY_TEMPLATE = (
    "SELECT TOP {limit} pl_name, hostname, sy_snum, sy_vmag, sy_dist, st_spectype "
    "FROM ps "
    "WHERE sy_vmag IS NOT NULL AND sy_dist IS NOT NULL "
    "ORDER BY sy_vmag ASC"
)
DISTANCE_PC_TO_LY = 3.26156
MAX_RETRIES = 3
RETRY_BACKOFF_SECONDS = 2


class NASAExoplanetClient:
    """Small helper that fetches/caches exoplanet host star data."""

    def __init__(
        self,
        cache_path: Path | None = None,
        ttl_seconds: int | None = None,
        max_records: int | None = None,
        *,
        http_timeout: float = 60.0,
    ) -> None:
        self.cache_path = cache_path or settings.nasa_cache_path
        self.ttl_seconds = ttl_seconds or settings.nasa_cache_ttl_seconds
        self.max_records = max_records or settings.nasa_max_records
        self.http_timeout = http_timeout

    def get_objects(self, *, force_refresh: bool = False) -> List[dict[str, Any]]:
        """Return cached or freshly fetched objects."""

        cached = None if force_refresh else self._load_cache()
        if cached is not None:
            LOGGER.debug("Loaded %s cached records from %s", len(cached), self.cache_path)
            return cached

        try:
            records = list(self._fetch_remote())
        except Exception:
            if cached is not None:
                LOGGER.warning("Remote fetch failed, returning cached data", exc_info=True)
                return cached
            raise

        self._write_cache(records)
        return records

    # ------------------------------------------------------------------
    def _fetch_remote(self) -> Iterable[dict[str, Any]]:
        import time
        query = QUERY_TEMPLATE.format(limit=self.max_records)
        LOGGER.info("Fetching exoplanet data from NASA (limit=%s)", self.max_records)
        
        for attempt in range(MAX_RETRIES):
            try:
                with httpx.Client(timeout=self.http_timeout) as client:
                    response = client.get(EXOPLANET_ENDPOINT, params={"query": query, "format": "json"})
                    response.raise_for_status()
                    payload = response.json()
                LOGGER.info("Fetched %s rows from NASA", len(payload))
                return payload
            except (httpx.TimeoutException, httpx.ConnectError) as exc:
                if attempt < MAX_RETRIES - 1:
                    wait_time = RETRY_BACKOFF_SECONDS * (2 ** attempt)
                    LOGGER.warning(
                        "NASA fetch attempt %s/%s failed, retrying in %ss",
                        attempt + 1,
                        MAX_RETRIES,
                        wait_time,
                        exc_info=True
                    )
                    time.sleep(wait_time)
                else:
                    LOGGER.error("NASA fetch failed after %s attempts", MAX_RETRIES)
                    raise

    def _load_cache(self) -> List[dict[str, Any]] | None:
        if not self.cache_path.exists():
            return None
        try:
            with self.cache_path.open("r", encoding="utf-8") as handle:
                cache_payload = json.load(handle)
        except json.JSONDecodeError:
            LOGGER.warning("Cache file %s is corrupt; ignoring", self.cache_path)
            return None

        expires_at = cache_payload.get("expires_at")
        if not expires_at:
            return None
        if datetime.now(timezone.utc) >= datetime.fromisoformat(expires_at):
            LOGGER.info("Cache at %s expired", self.cache_path)
            return None
        return cache_payload.get("records", [])

    def _write_cache(self, records: Sequence[dict[str, Any]]) -> None:
        payload = {
            "records": list(records),
            "fetched_at": datetime.now(timezone.utc).isoformat(),
            "expires_at": (datetime.now(timezone.utc) + timedelta(seconds=self.ttl_seconds)).isoformat(),
        }
        self.cache_path.parent.mkdir(parents=True, exist_ok=True)
        with self.cache_path.open("w", encoding="utf-8") as handle:
            json.dump(payload, handle)


NASA_CLIENT = NASAExoplanetClient()
