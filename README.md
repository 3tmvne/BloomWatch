# BloomWatch 🌸

An Earth Observation application for detecting, tracking, and forecasting flowering phenology using multi-sensor satellite imagery and climate data.

## Vision
Provide researchers, ecologists, and the public with near-real-time and historical insights into flowering dynamics, enabling analysis of climate trends, ecosystem shifts, and species-specific phenology signals.

## Initial MVP Goal
Process a small Sentinel-2 sample for a defined Area of Interest (AOI), compute NDVI time series, derive a simple bloom indicator, and serve it through an API + minimal frontend view.

## Roadmap (Phase 0 → Phase 2)
- Phase 0: Repository scaffolding, NDVI computation, baseline bloom heuristic
- Phase 1: STAC search + multi-date ingestion, time series smoothing, map visualization
- Phase 2: ML prototype (temporal model), uncertainty estimates, species layering (optional)

## Tech Stack (proposed)
- Backend API: FastAPI
- Processing / ML: Python (rasterio, numpy, geopandas, torch)
- Frontend (future): React + MapLibre or Next.js
- CI: GitHub Actions (lint + tests)
- Container: Docker (Python 3.11-slim)

## Directory Structure
```
bloomwatch/
  api/
  src/
  data/
  models/
  frontend/
  notebooks/
  tests/
  docs/
```

## Quickstart (after first commit)
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn api.main:app --reload
```
Visit: http://127.0.0.1:8000/health

## Next Steps
1. Implement STAC search + sample ingestion
2. Add NDVI time series example
3. Add basic bloom heuristic
4. Build minimal frontend map

## Licensing
TBD (recommend Apache-2.0 unless constraints dictate otherwise)

## Contributing
See CONTRIBUTING.md (to be added).