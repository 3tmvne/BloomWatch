from fastapi import FastAPI, HTTPException
from datetime import datetime, timedelta
from typing import Any
import numpy as np

from src.stac_search import search_sentinel2_data
from src.ndvi_processor import calculate_ndvi

app = FastAPI(
    title="BloomWatch API",
    description="API for detecting, tracking, and forecasting flowering phenology.",
    version="0.1.0",
)

# A simple in-memory cache to store search results temporarily
search_cache = {}

@app.get("/health", tags=["Status"])
async def health_check():
    """Confirms the API service is running."""
    return {"status": "ok", "message": "BloomWatch API is healthy!"}

@app.post("/search", tags=["Data"])
async def search_data(aoi: dict[str, Any]):
    """Performs a STAC search and caches the results."""
    try:
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=30)
        items = search_sentinel2_data(aoi, (start_date, end_date))

        if not items:
            raise HTTPException(status_code=404, detail="No items found.")
        
        # Cache the found items by their ID
        for item in items:
            search_cache[item.id] = item

        item_summaries = []
        for item in items:
            thumbnail_asset = item.assets.get("thumbnail")
            item_summaries.append({
                "id": item.id,
                "datetime": item.datetime,
                "cloud_cover": item.properties.get("eo:cloud_cover"),
                "thumbnail_url": thumbnail_asset.href if thumbnail_asset else None,
            })
        
        return {"search_results": item_summaries}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An internal error occurred: {e}")

@app.post("/process/{item_id}", tags=["Processing"])
async def process_item(item_id: str):
    """
    Calculates NDVI for a specific STAC item found via the /search endpoint.
    """
    # Find the item in our simple cache
    item = search_cache.get(item_id)
    if not item:
        raise HTTPException(status_code=404, detail=f"Item '{item_id}' not found. Please run a /search first.")

    try:
        # Calculate NDVI
        ndvi_array = calculate_ndvi(item)

        # Return statistics about the NDVI array instead of the whole array
        return {
            "item_id": item_id,
            "message": "NDVI calculation successful.",
            "ndvi_stats": {
                "min": float(np.min(ndvi_array)),
                "max": float(np.max(ndvi_array)),
                "mean": float(np.mean(ndvi_array)),
                "shape": ndvi_array.shape
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process item {item_id}: {e}")
