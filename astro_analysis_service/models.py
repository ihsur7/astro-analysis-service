"""Pydantic models used by the API."""
from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


class AstronomicalObject(BaseModel):
    id: int
    name: str
    constellation: str
    magnitude: float
    distance_ly: float = Field(..., description="Distance in light years")
    spectral_type: str


class ObjectQueryParams(BaseModel):
    magnitude_min: float | None = Field(None, description="Minimum apparent magnitude (dimmer)")
    magnitude_max: float | None = Field(None, description="Maximum apparent magnitude (brighter)")
    distance_min: float | None = Field(None, description="Minimum distance in light years")
    distance_max: float | None = Field(None, description="Maximum distance in light years")
    constellation: str | None = Field(None, description="Exact constellation match (case-insensitive)")
    spectral_type: str | None = Field(None, description="Exact spectral class match (case-insensitive)")
    search: str | None = Field(None, description="Substring match against name or constellation")


class PaginatedObjectsResponse(BaseModel):
    total: int = Field(..., ge=0)
    page: int = Field(..., ge=1)
    page_size: int = Field(..., ge=1)
    pages: int = Field(..., ge=0)
    items: list[AstronomicalObject]


class StatsResponse(BaseModel):
    count: int
    magnitude_min: float | None
    magnitude_max: float | None
    magnitude_avg: float | None
    brightest_object: AstronomicalObject | None
    dimmest_object: AstronomicalObject | None


class HealthResponse(BaseModel):
    status: Literal["ok", "error"]
    service: str
    version: str


class ReadinessResponse(HealthResponse):
    dataset_count: int | None = Field(None, ge=0)
