# Astro Analysis Service

[![CI](https://github.com/ihsur7/astro-analysis-service/actions/workflows/ci.yml/badge.svg)](https://github.com/ihsur7/astro-analysis-service/actions/workflows/ci.yml)
[![Build Singularity](https://github.com/ihsur7/astro-analysis-service/actions/workflows/singularity.yml/badge.svg)](https://github.com/ihsur7/astro-analysis-service/actions/workflows/singularity.yml)

FastAPI microservice delivering real-time exoplanet system data from the NASA Exoplanet Archive. Provides filtered queries, statistical summaries, and a modern Vue 3 frontend for exploring thousands of confirmed exoplanet hosts.

## Features

### API Layer
- **Paginated catalog** (`/objects`) with query filters: magnitude range, distance bounds, constellation, spectral type, fuzzy search
- **Statistical summary** (`/stats`) reporting dataset count, magnitude extremes, and brightest/dimmest objects
- **Health endpoints** (`/health`, `/ready`) for orchestrator liveness/readiness checks
- **Prometheus metrics** (`/metrics`) exposing request latency histograms, throughput counters, dataset gauge
- **Structured logging** JSON-formatted logs with request IDs and duration headers (`X-Process-Time`, `X-Request-ID`)

### Data Integration
- **NASA Exoplanet Archive TAP client** querying the `ps` (Planetary Systems) table for host-star photometry, distance, and spectral classification
- **Resilient networking**: 60-second timeout, 3-retry exponential backoff (2s/4s/8s delays)
- **JSON cache** with configurable TTL (default 24h) for offline resilience

### Frontend
- **Vue 3 SPA** (TypeScript + Vite + Pinia) with:
  - `FiltersPanel`: magnitude/distance sliders, constellation/spectral dropdowns, search input
  - `StatsPanel`: live count, magnitude range, brightest object highlight
  - `ObjectsTable`: responsive cards showing name, magnitude, distance, spectral type
  - `PaginationControls`: page size selector, page navigation
  - `StatusBar`: fetch status, error messages, refresh trigger
- **Hot-reload dev server** proxying API calls for rapid iteration
- **Production build** bundled into FastAPI static assets (served at `/`)

### DevOps
- **Docker** multi-stage build (frontend → backend → slim runtime)
- **Singularity/Apptainer** definition file for HPC deployments
- **GitHub Actions CI** pipelines:
  - Backend tests → frontend build → Docker image
  - Singularity container build from definition file
- **pytest suite** mocking NASA responses (8 passing tests, no external dependencies)

## Getting Started

### Install Dependencies

#### PowerShell
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install -e .[dev]
```

#### Bash
```bash
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -e .[dev]
```

### Run API Locally

```bash
uvicorn astro_analysis_service.main:app --reload
```

Visit `http://127.0.0.1:8000/docs` for interactive API documentation.

## Configuration

Control NASA data fetching via environment variables:

| Variable | Default | Description |
| --- | --- | --- |
| `NASA_CACHE_TTL_SECONDS` | `86400` | Cache validity period (seconds) |
| `NASA_MAX_RECORDS` | `150` | TAP query result limit |
| `NASA_CACHE_PATH` | `astro_analysis_service/data/cache/nasa_exoplanets.json` | Cache file location |

## API Reference

### GET `/objects`

Paginated catalog with filters.

**Query Parameters:**
| Parameter | Type | Description |
| --- | --- | --- |
| `page` | int | Page number (1-indexed) |
| `page_size` | int | Results per page (1–100) |
| `magnitude_min` | float | Minimum apparent magnitude |
| `magnitude_max` | float | Maximum apparent magnitude |
| `distance_min` | float | Minimum distance (light years) |
| `distance_max` | float | Maximum distance (light years) |
| `constellation` | string | Exact constellation match (case-insensitive) |
| `spectral_type` | string | Exact spectral type match (case-insensitive) |
| `search` | string | Fuzzy search across name/constellation |

**Response:**
```json
{
  "total": 150,
  "page": 1,
  "page_size": 25,
  "pages": 6,
  "items": [
    {
      "id": 1,
      "name": "Kepler-1649 c",
      "constellation": "2",
      "magnitude": 3.45,
      "distance_ly": 301.234,
      "spectral_type": "M5 V"
    }
  ]
}
```

### GET `/stats`

Dataset statistical summary.

**Response:**
```json
{
  "total_objects": 150,
  "magnitude_range": {"min": -1.46, "max": 12.34, "avg": 6.78},
  "brightest": "Sirius",
  "dimmest": "Proxima Centauri"
}
```

### GET `/health`

Liveness probe.

**Response:**
```json
{
  "status": "healthy",
  "service": "astro-analysis-service",
  "version": "1.0.0"
}
```

### GET `/ready`

Readiness probe verifying dataset availability.

**Response:**
```json
{
  "status": "ready",
  "dataset_count": 150
}
```

### GET `/metrics`

Prometheus-formatted metrics including:
- `http_requests_total` (counter, labeled by method/path/status)
- `http_request_duration_seconds` (histogram)
- `astro_dataset_objects_total` (gauge, dataset size)

## Frontend Development

### Dev Server
```bash
cd frontend
npm install
npm run dev
```
Access at `http://localhost:5173` with API calls proxied to `http://127.0.0.1:8000`.

### Production Build
```bash
cd frontend
npm run build
```
Outputs to `../astro_analysis_service/static/app/`, served by FastAPI at `/`.

## Testing

Run pytest suite (mocks NASA API):
```bash
pytest -q
```

Expected output: `8 passed` (tests cover `/objects`, `/stats`, `/health`, `/ready`, NASA client retry logic).

## Container Images

### Docker

#### Build Image
```bash
docker build -t astro-analysis-service .
```

#### Run Container
```bash
docker run -p 8000:8000 astro-analysis-service
```

Access API at `http://localhost:8000/docs`, SPA at `http://localhost:8000/`.

### Singularity/Apptainer

For HPC environments and reproducible scientific computing.

#### Download Pre-built Image

```bash
# Download from GitHub Releases
wget https://github.com/ihsur7/astro-analysis-service/releases/latest/download/astro-analysis.sif
```

#### Build from Definition File

```bash
# Requires root/sudo privileges
singularity build astro-analysis.sif Singularity.def

# Or using Apptainer
apptainer build astro-analysis.sif Singularity.def
```

#### Build from Docker Image

```bash
# Build Docker image first
docker build -t astro-analysis-service:latest .

# Export to tar
docker save astro-analysis-service:latest -o astro-analysis.tar

# Convert to Singularity
singularity build astro-analysis.sif docker-archive://astro-analysis.tar
```

#### Run Singularity Container

```bash
# Run the service (default port 8000)
singularity run astro-analysis.sif

# Custom port
PORT=9000 singularity run astro-analysis.sif

# With custom data directory binding
singularity run --bind ./custom-data:/app/data astro-analysis.sif

# Execute specific commands
singularity exec astro-analysis.sif python -m pytest

# Interactive shell
singularity shell astro-analysis.sif

# View help
singularity run-help astro-analysis.sif
```

**Endpoints:**
- Web UI: `http://localhost:8000/`
- API Docs: `http://localhost:8000/docs`
- Health Check: `http://localhost:8000/health`
- Metrics: `http://localhost:8000/metrics`

## Architecture Notes

- **Data Source**: NASA Exoplanet Archive TAP service (`https://exoplanetarchive.ipac.caltech.edu/TAP/sync`)
- **Query**: `SELECT TOP {limit} pl_name, hostname, sy_snum, sy_vmag, sy_dist, st_spectype FROM ps WHERE sy_vmag IS NOT NULL AND sy_dist IS NOT NULL ORDER BY sy_vmag ASC`
- **Cache Strategy**: 24h TTL JSON file, stale-while-revalidate on startup
- **Error Handling**: Exponential backoff retries prevent transient network failures from breaking service
- **Frontend State**: Pinia store (`catalog.ts`) manages API calls, pagination, filters via axios
- **Observability**: Prometheus instrumentation via `prometheus-fastapi-instrumentator`, JSON logs for structured ingestion

## License

MIT
