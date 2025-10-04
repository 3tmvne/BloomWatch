from fastapi import FastAPI, HTTPException
from datetime import datetime, timedelta
from typing import Any
import numpy as np

# Import the new function and remove the cache
from src.stac_search import search_sentinel2_data, get_item_by_id
from src.ndvi_processor import calculate_ndvi

app = FastAPI(
    title="BloomWatch API",
    description="API for detecting, tracking, and forecasting flowering phenology.",
    version="0.1.0",
)

# The in-memory cache is no longer needed and can be removed.
# search_cache = {} 

@app.get("/health", tags=["Status"])
async def health_check():
    """Confirms the API service is running."""
    return {"status": "ok", "message": "BloomWatch API is healthy!"}

@app.post("/search", tags=["Data"])
async def search_data(aoi: dict[str, Any]):
    """Performs a STAC search."""
    try:
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=30)
        items = search_sentinel2_data(aoi, (start_date, end_date))

        if not items:
            raise HTTPException(status_code=404, detail="No items found.")
        
        # No need to cache results anymore. Just return the summary.
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
    Fetches a STAC item by ID and calculates its NDVI. This is now stateless.
    """
    # --- UPDATED LOGIC ---
    # Fetch the item directly instead of looking in a cache.
    item = get_item_by_id(item_id)
    if not item:
        raise HTTPException(status_code=404, detail=f"Item '{item_id}' could not be found in the Planetary Computer catalog.")

    try:
        ndvi_array = calculate_ndvi(item)
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
