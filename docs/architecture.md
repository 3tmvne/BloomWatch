# BloomWatch Architecture Overview

## High-Level Components
1. Ingestion Layer: STAC search + data retrieval (Sentinel-2, Landsat).
2. Preprocessing Pipeline: Cloud masking (future), spectral index computation (NDVI, EVI), temporal aggregation.
3. Phenology Analysis: Baseline heuristics (slope/threshold), future ML temporal models.
4. API Service: FastAPI exposing health, bloom query, time series endpoints (future).
5. Frontend Client: Interactive map + charts (future React/MapLibre).
6. Storage: Local filesystem (dev) → object storage (future).

## Data Flow
Raw Imagery -> Preprocess -> Indices Time Series -> Phenology Detection -> API Responses -> Frontend Visualization

## Future Enhancements
- Caching layer for tile/time queries
- ML model registry
- Streaming updates via WebSocket

## Security & Scaling (Future)
- Auth for write endpoints
- Rate limiting
- Horizontal scaling via containers

## Next Steps
- Implement STAC search abstraction
- Add AOI management
- Integrate baseline bloom detector
