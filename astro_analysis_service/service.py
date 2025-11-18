"""Core filtering and statistics logic for the API."""
from __future__ import annotations

from collections import Counter
from math import ceil
from statistics import mean
from typing import Dict, Iterable, List, Sequence, Tuple

from .data_loader import load_objects
from .models import AstronomicalObject, StatsResponse


def filter_objects(
    magnitude_min: float | None = None,
    magnitude_max: float | None = None,
    distance_min: float | None = None,
    distance_max: float | None = None,
    constellation: str | None = None,
    spectral_type: str | None = None,
    search: str | None = None,
) -> List[AstronomicalObject]:
    objects = load_objects()
    constellation_lower = constellation.lower() if constellation else None
    spectral_lower = spectral_type.lower() if spectral_type else None
    search_lower = search.lower() if search else None

    def passes_filters(obj: AstronomicalObject) -> bool:
        if magnitude_min is not None and obj.magnitude < magnitude_min:
            return False
        if magnitude_max is not None and obj.magnitude > magnitude_max:
            return False
        if distance_min is not None and obj.distance_ly < distance_min:
            return False
        if distance_max is not None and obj.distance_ly > distance_max:
            return False
        if constellation_lower and obj.constellation.lower() != constellation_lower:
            return False
        if spectral_lower and obj.spectral_type.lower() != spectral_lower:
            return False
        if search_lower and search_lower not in f"{obj.name.lower()} {obj.constellation.lower()}":
            return False
        return True

    return [obj for obj in objects if passes_filters(obj)]


def paginate_objects(
    objects: Sequence[AstronomicalObject],
    page: int,
    page_size: int,
) -> Tuple[List[AstronomicalObject], int, int]:
    total = len(objects)
    if total == 0:
        return [], 0, 0

    pages = ceil(total / page_size)
    start = (page - 1) * page_size
    if start >= total:
        return [], total, pages

    end = start + page_size
    return list(objects[start:end]), total, pages


def compute_stats(objects: Iterable[AstronomicalObject] | None = None) -> StatsResponse:
    dataset = list(objects) if objects is not None else load_objects()
    if not dataset:
        return StatsResponse(
            count=0,
            magnitude_min=None,
            magnitude_max=None,
            magnitude_avg=None,
            brightest_object=None,
            dimmest_object=None,
        )

    magnitudes = [obj.magnitude for obj in dataset]
    brightest = min(dataset, key=lambda obj: obj.magnitude)
    dimmest = max(dataset, key=lambda obj: obj.magnitude)

    return StatsResponse(
        count=len(dataset),
        magnitude_min=min(magnitudes),
        magnitude_max=max(magnitudes),
        magnitude_avg=mean(magnitudes),
        brightest_object=brightest,
        dimmest_object=dimmest,
    )


def get_magnitude_distribution(bins: int = 10) -> Dict[str, List[float | int]]:
    """Calculate magnitude distribution histogram."""
    dataset = load_objects()
    if not dataset:
        return {"bins": [], "counts": []}

    magnitudes = [obj.magnitude for obj in dataset]
    min_mag = min(magnitudes)
    max_mag = max(magnitudes)
    bin_width = (max_mag - min_mag) / bins

    bin_edges = [min_mag + i * bin_width for i in range(bins + 1)]
    bin_labels = [round((bin_edges[i] + bin_edges[i + 1]) / 2, 2) for i in range(bins)]
    counts = [0] * bins

    for mag in magnitudes:
        if mag == max_mag:
            counts[-1] += 1
        else:
            bin_idx = int((mag - min_mag) / bin_width)
            counts[bin_idx] += 1

    return {"bins": bin_labels, "counts": counts}


def get_spectral_type_breakdown() -> Dict[str, int]:
    """Count objects by spectral type."""
    dataset = load_objects()
    spectral_counts = Counter(obj.spectral_type for obj in dataset if obj.spectral_type)
    return dict(spectral_counts.most_common())


def get_distance_distribution(bins: int = 10) -> Dict[str, List[float | int]]:
    """Calculate distance distribution histogram."""
    dataset = load_objects()
    if not dataset:
        return {"bins": [], "counts": []}

    distances = [obj.distance_ly for obj in dataset]
    min_dist = min(distances)
    max_dist = max(distances)
    bin_width = (max_dist - min_dist) / bins

    bin_edges = [min_dist + i * bin_width for i in range(bins + 1)]
    bin_labels = [round((bin_edges[i] + bin_edges[i + 1]) / 2, 1) for i in range(bins)]
    counts = [0] * bins

    for dist in distances:
        if dist == max_dist:
            counts[-1] += 1
        else:
            bin_idx = int((dist - min_dist) / bin_width)
            counts[bin_idx] += 1

    return {"bins": bin_labels, "counts": counts}


def get_magnitude_distance_correlation() -> Dict[str, List[float]]:
    """Get magnitude-distance data points for scatter plot."""
    dataset = load_objects()
    return {
        "magnitudes": [obj.magnitude for obj in dataset],
        "distances": [obj.distance_ly for obj in dataset],
    }
