from fastapi import FastAPI, HTTPException
from datetime import datetime, timedelta
from typing import Any
import numpy as np

from src.stac_search import search_sentinel2_data, get_item_by_id
from src.ndvi_processor import calculate_ndvi
from src.phenology import classify_vegetation_state # <-- Import the new function

app = FastAPI(
    title="BloomWatch API",
    description="API for detecting, tracking, and forecasting flowering phenology.",
    version="0.1.0",
)

# ... (all other endpoints remain the same) ...

@app.post("/process/{item_id}", tags=["Processing"])
async def process_item(item_id: str):
    """
    Fetches a STAC item, calculates NDVI, and classifies the vegetation state.
    """
    item = get_item_by_id(item_id)
    if not item:
        raise HTTPException(status_code=404, detail=f"Item '{item_id}' could not be found.")

    try:
        # Step 1: Calculate NDVI
        ndvi_array = calculate_ndvi(item)
        
        # Step 2: Classify the vegetation state using the heuristic
        vegetation_state = classify_vegetation_state(ndvi_array)

        # Step 3: Return the results
        return {
            "item_id": item_id,
            "message": "Processing successful.",
            "vegetation_state": vegetation_state, # <-- Add the new result
            "ndvi_stats": {
                "min": float(np.min(ndvi_array)),
                "max": float(np.max(ndvi_array)),
                "mean": float(np.mean(ndvi_array)),
                "shape": ndvi_array.shape
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process item {item_id}: {e}")
