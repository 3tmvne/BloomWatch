import numpy as np

# Define a simple threshold for our heuristic.
# Values are from -1 to 1. 0.4 is a reasonable starting point for healthy vegetation.
NDVI_THRESHOLD = 0.4

def classify_vegetation_state(ndvi_array: np.ndarray) -> str:
    """
    Classifies the vegetation state based on the average NDVI value.

    Args:
        ndvi_array (np.ndarray): The array of NDVI values.

    Returns:
        str: A string classifying the vegetation state.
    """
    # Calculate the mean NDVI, ignoring NaN or zero values which can skew the result
    mean_ndvi = np.mean(ndvi_array[ndvi_array > 0])

    if mean_ndvi > NDVI_THRESHOLD:
        return "High Vegetation"
    else:
        return "Low Vegetation"
