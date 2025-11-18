from __future__ import annotations

from pathlib import Path

import pytest

from astro_analysis_service.data_loader import _api_record_to_object
from astro_analysis_service.nasa_client import DISTANCE_PC_TO_LY, NASAExoplanetClient


@pytest.fixture()
def sample_records():
    return [
        {
            "pl_name": "Kepler-22 b",
            "hostname": "Kepler-22",
            "sy_snum": "1",
            "sy_vmag": "11.664",
            "sy_dist": "195.0",
            "st_spectype": "G5",
        }
    ]


def test_nasa_client_uses_cache(tmp_path: Path, sample_records):
    cache_path = tmp_path / "cache.json"
    client = NASAExoplanetClient(cache_path=cache_path, ttl_seconds=60)

    # Force a refresh to populate cache
    def fake_fetch():
        return sample_records

    client._fetch_remote = fake_fetch  # type: ignore[attr-defined]
    fetched = client.get_objects(force_refresh=True)
    assert fetched == sample_records
    assert cache_path.exists()

    # Break remote fetch to ensure cache is used
    def _raise():  # pragma: no cover - behavior validated via cache hit
        raise AssertionError("Should not hit network")

    client._fetch_remote = _raise  # type: ignore[attr-defined]
    cached = client.get_objects()
    assert cached == sample_records


def test_api_record_conversion(sample_records):
    obj = _api_record_to_object(sample_records[0], idx=1)
    assert obj is not None
    assert obj.name == "Kepler-22 b"
    assert obj.constellation == "1"
    assert obj.spectral_type == "G5"
    assert obj.magnitude == pytest.approx(11.664)
    assert obj.distance_ly == pytest.approx(195.0 * DISTANCE_PC_TO_LY, rel=1e-5)