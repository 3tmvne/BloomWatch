from fastapi import FastAPI, HTTPException
from datetime import datetime, timedelta
from typing import Any

# Assuming your src folder is in the python path
from src.stac_search import search_sentinel2_data

# Create an instance of the FastAPI class
app = FastAPI(
    title="BloomWatch API",
    description="API for detecting, tracking, and forecasting flowering phenology.",
    version="0.1.0",
)

@app.get("/health", tags=["Status"])
async def health_check():
    """
    A simple endpoint to confirm that the API service is running.
    """
    return {"status": "ok", "message": "BloomWatch API is healthy!"}

@app.post("/search", tags=["Data"])
async def search_data(aoi: dict[str, Any]):
    """
    Performs a STAC search for Sentinel-2 data for the given Area of Interest (AOI).
    The search covers the last 30 days.

    Args:
        aoi (dict): A GeoJSON dictionary (e.g., Point, Polygon) for the search area.
    
    Returns:
        A list of STAC item summaries.
    """
    try:
        # Define a 30-day date range for the search
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=30)
        
        # Perform the search
        items = search_sentinel2_data(aoi, (start_date, end_date))

        if items is None or not items:
            raise HTTPException(status_code=404, detail="No items found for the given AOI and date range.")

        # Return a simplified summary of the found items
        item_summaries = [
            {
                "id": item.id,
                "datetime": item.datetime,
                "cloud_cover": item.properties.get("eo:cloud_cover"),
                "thumbnail_url": item.assets.get("thumbnail", {}).href,
            }
            for item in items
        ]
        
        return {"search_results": item_summaries}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

