from fastapi import FastAPI

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

