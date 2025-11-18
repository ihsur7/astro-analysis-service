"""FastAPI application entrypoint."""
from __future__ import annotations

import logging
import time
import uuid
from pathlib import Path

from fastapi import FastAPI, HTTPException, Query, Request, status
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from prometheus_client import Gauge
from prometheus_fastapi_instrumentator import Instrumentator

from .data_loader import load_objects
from .logging_config import configure_logging
from .models import HealthResponse, PaginatedObjectsResponse, ReadinessResponse, StatsResponse
from .service import compute_stats, filter_objects, paginate_objects

BASE_DIR = Path(__file__).resolve().parent
FRONTEND_DIST = BASE_DIR / "static" / "app"
FRONTEND_INDEX = FRONTEND_DIST / "index.html"
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))
configure_logging()
logger = logging.getLogger("astro.analysis.api")
DATASET_GAUGE = Gauge(
    "astro_dataset_objects_total",
    "Number of astronomical objects currently cached and available to the API.",
)

app = FastAPI(title="Astro Analysis Service", version="0.1.0")

if FRONTEND_DIST.exists():
    app.mount("/app", StaticFiles(directory=str(FRONTEND_DIST), html=True), name="spa")

Instrumentator().instrument(app).expose(app, endpoint="/metrics", include_in_schema=False)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    request_id = request.headers.get("x-request-id", str(uuid.uuid4()))
    start = time.perf_counter()
    response = await call_next(request)
    duration_ms = (time.perf_counter() - start) * 1000
    logger.info(
        "request",
        extra={
            "extra_data": {
                "request_id": request_id,
                "path": request.url.path,
                "method": request.method,
                "status_code": response.status_code,
                "duration_ms": round(duration_ms, 2),
            }
        },
    )
    response.headers["X-Request-ID"] = request_id
    response.headers["X-Process-Time"] = f"{duration_ms:.2f}ms"
    return response


@app.get("/", include_in_schema=False)
def dashboard(request: Request):
    if FRONTEND_INDEX.exists():
        return FileResponse(FRONTEND_INDEX)
    return templates.TemplateResponse("terminal.html", {"request": request})


@app.get("/ui", include_in_schema=False, response_class=HTMLResponse)
def legacy_dashboard(request: Request):
    return templates.TemplateResponse("terminal.html", {"request": request})


@app.get("/objects", response_model=PaginatedObjectsResponse)
def list_objects(
    magnitude_min: float | None = Query(None, description="Include stars with magnitude >= this value (dimmer)."),
    magnitude_max: float | None = Query(None, description="Include stars with magnitude <= this value (brighter)."),
    distance_min: float | None = Query(None, description="Include stars farther than this distance (light years)."),
    distance_max: float | None = Query(None, description="Include stars closer than this distance (light years)."),
    constellation: str | None = Query(None, description="Exact constellation code (case-insensitive)."),
    spectral_type: str | None = Query(None, description="Exact spectral class (case-insensitive)."),
    search: str | None = Query(None, description="Substring match against name or constellation."),
    page: int = Query(1, ge=1, description="Page number (1-indexed)."),
    page_size: int = Query(25, ge=1, le=100, description="Number of rows per page."),
):
    filtered = filter_objects(
        magnitude_min=magnitude_min,
        magnitude_max=magnitude_max,
        distance_min=distance_min,
        distance_max=distance_max,
        constellation=constellation,
        spectral_type=spectral_type,
        search=search,
    )
    items, total, pages = paginate_objects(filtered, page=page, page_size=page_size)
    return PaginatedObjectsResponse(
        items=items,
        total=total,
        page=page,
        page_size=page_size,
        pages=pages,
    )


@app.get("/stats", response_model=StatsResponse)
def stats():
    return compute_stats()


@app.get("/health", response_model=HealthResponse, tags=["Health"])
def health() -> HealthResponse:
    return HealthResponse(status="ok", service="astro-analysis-service", version=app.version)


@app.get("/ready", response_model=ReadinessResponse, tags=["Health"])
def readiness() -> ReadinessResponse:
    try:
        dataset = load_objects()
    except Exception as exc:  # pragma: no cover - surfaced through response
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={"status": "error", "reason": str(exc)},
        ) from exc

    DATASET_GAUGE.set(len(dataset))

    return ReadinessResponse(
        status="ok",
        service="astro-analysis-service",
        version=app.version,
        dataset_count=len(dataset),
    )
