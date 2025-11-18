import pytest
from fastapi.testclient import TestClient

from astro_analysis_service import data_loader
from astro_analysis_service.main import app
from astro_analysis_service.models import AstronomicalObject


@pytest.fixture(autouse=True)
def mock_nasa_dataset(monkeypatch):
    """Provide a deterministic mock dataset for API tests."""
    mock_data = [
        AstronomicalObject(id=1, name="Sirius", constellation="Canis Major", magnitude=-1.46, distance_ly=8.6, spectral_type="A1V"),
        AstronomicalObject(id=2, name="Canopus", constellation="Carina", magnitude=-0.74, distance_ly=310, spectral_type="B8Ia"),
        AstronomicalObject(id=3, name="Arcturus", constellation="Bootes", magnitude=-0.05, distance_ly=36.7, spectral_type="K1.5III"),
        AstronomicalObject(id=4, name="Vega", constellation="Lyra", magnitude=0.03, distance_ly=25.0, spectral_type="A0V"),
        AstronomicalObject(id=5, name="Capella", constellation="Auriga", magnitude=0.08, distance_ly=42.9, spectral_type="G5III"),
        AstronomicalObject(id=6, name="Rigel", constellation="Orion", magnitude=0.12, distance_ly=860.0, spectral_type="B8Ia"),
        AstronomicalObject(id=7, name="Procyon", constellation="Canis Minor", magnitude=0.38, distance_ly=11.5, spectral_type="F5IV-V"),
        AstronomicalObject(id=8, name="Achernar", constellation="Eridanus", magnitude=0.46, distance_ly=139.0, spectral_type="B6Vep"),
        AstronomicalObject(id=9, name="Betelgeuse", constellation="Orion", magnitude=0.42, distance_ly=642.0, spectral_type="M2Iab"),
        AstronomicalObject(id=10, name="Altair", constellation="Aquila", magnitude=0.77, distance_ly=16.7, spectral_type="A7V"),
    ]
    data_loader.load_objects.cache_clear()
    monkeypatch.setattr("astro_analysis_service.data_loader._load_from_nasa", lambda **kwargs: mock_data)
    yield
    data_loader.load_objects.cache_clear()


client = TestClient(app)


def test_list_objects_filters_by_magnitude():
    response = client.get("/objects", params={"magnitude_max": 0.1})
    assert response.status_code == 200
    payload = response.json()
    assert payload["total"] > 0
    assert payload["items"]
    assert all(obj["magnitude"] <= 0.1 for obj in payload["items"])


def test_list_objects_supports_new_filters_and_search():
    response = client.get(
        "/objects",
        params={
            "constellation": "orion",
            "spectral_type": "b8ia",
        },
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["total"] == 1
    assert payload["items"][0]["name"] == "Rigel"

    search_response = client.get("/objects", params={"search": "orion"})
    assert search_response.status_code == 200
    search_payload = search_response.json()
    assert search_payload["total"] == 2  # Rigel + Betelgeuse


def test_list_objects_paginates_results():
    response = client.get("/objects", params={"page": 2, "page_size": 3})
    assert response.status_code == 200
    payload = response.json()
    assert payload["page"] == 2
    assert payload["page_size"] == 3
    assert payload["total"] == 10
    assert len(payload["items"]) == 3


def test_stats_endpoint_returns_summary():
    response = client.get("/stats")
    assert response.status_code == 200
    payload = response.json()
    assert payload["count"] == 10
    assert payload["magnitude_min"] <= payload["magnitude_max"]
    assert payload["brightest_object"]
    assert payload["dimmest_object"]


def test_health_endpoints():
    health = client.get("/health")
    assert health.status_code == 200
    assert health.json()["status"] == "ok"

    ready = client.get("/ready")
    assert ready.status_code == 200
    body = ready.json()
    assert body["status"] == "ok"
    assert body["dataset_count"] == 10


def test_metrics_endpoint_exposes_dataset_gauge():
    response = client.get("/metrics")
    assert response.status_code == 200
    assert "astro_dataset_objects_total" in response.text
