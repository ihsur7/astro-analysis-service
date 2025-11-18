"""Utilities for loading the astronomical dataset from NASA Exoplanet Archive."""
from __future__ import annotations

import logging
from functools import lru_cache
from typing import List

from .models import AstronomicalObject
from .nasa_client import NASA_CLIENT, DISTANCE_PC_TO_LY

LOGGER = logging.getLogger(__name__)


def _api_record_to_object(record: dict[str, str], idx: int) -> AstronomicalObject | None:
    magnitude = _parse_float(record.get("sy_vmag"))
    distance_pc = _parse_float(record.get("sy_dist"))
    if magnitude is None or distance_pc is None:
        return None

    name = (record.get("pl_name") or record.get("hostname") or f"Object {idx}").strip()
    constellation = str(record.get("sy_snum", "Unknown")).strip()
    spectral = (record.get("st_spectype") or "Unknown").strip()
    distance_ly = distance_pc * DISTANCE_PC_TO_LY

    return AstronomicalObject(
        id=idx,
        name=name,
        constellation=constellation,
        magnitude=magnitude,
        distance_ly=round(distance_ly, 3),
        spectral_type=spectral,
    )


def _parse_float(value: str | float | None) -> float | None:
    try:
        return float(value) if value not in (None, "") else None
    except (TypeError, ValueError):
        return None


def _load_from_nasa(force_refresh: bool = False) -> List[AstronomicalObject]:
    records = NASA_CLIENT.get_objects(force_refresh=force_refresh)
    objects: List[AstronomicalObject] = []
    for idx, record in enumerate(records, start=1):
        obj = _api_record_to_object(record, idx)
        if obj is not None:
            objects.append(obj)

    LOGGER.info("Loaded %s objects from NASA dataset", len(objects))
    return objects


@lru_cache(maxsize=1)
def load_objects(*, force_refresh: bool = False) -> List[AstronomicalObject]:
    return _load_from_nasa(force_refresh=force_refresh)
