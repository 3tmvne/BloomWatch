import rasterio
import numpy as np
from pystac.item import Item

def calculate_ndvi(item: Item) -> np.ndarray:
    """
    Calculates the NDVI array for a given Sentinel-2 STAC item.

    NDVI is calculated as (NIR - Red) / (NIR + Red).
    For Sentinel-2, Red is Band 4 and NIR is Band 8.

    Args:
        item (Item): A STAC item for a Sentinel-2 L2A scene.

    Returns:
        np.ndarray: A 2D numpy array containing the NDVI values.
    """
    try:
        # Get the URLs for the Red (B04) and NIR (B08) bands
        red_href = item.assets["B04"].href
        nir_href = item.assets["B08"].href

        # Open the bands using rasterio
        with rasterio.open(red_href) as red_src, rasterio.open(nir_href) as nir_src:
            # Read the data into numpy arrays
            red = red_src.read(1).astype(np.float32)
            nir = nir_src.read(1).astype(np.float32)

            # Calculate NDVI, avoiding division by zero
            # np.seterr suppresses warnings, which is fine here
            np.seterr(divide='ignore', invalid='ignore')
            ndvi = (nir - red) / (nir + red)
            
            # Replace NaNs that may have resulted from 0/0 division
            ndvi[np.isnan(ndvi)] = 0
            
            print(f"Successfully calculated NDVI for item {item.id}")
            return ndvi

    except Exception as e:
        print(f"Failed to calculate NDVI for item {item.id}. Error: {e}")
        raise
