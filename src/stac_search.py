from pystac_client import Client
from datetime import datetime

# URL for the Microsoft Planetary Computer STAC API
PLANETARY_COMPUTER_STAC_URL = "https://planetarycomputer.microsoft.com/api/stac/v1"

def search_sentinel2_data(aoi: dict, date_range: tuple[datetime, datetime]):
    """
    Searches the Planetary Computer for Sentinel-2 L2A data for a given
    Area of Interest (AOI) and date range.

    Args:
        aoi (dict): A GeoJSON dictionary representing the area of interest.
                    Example: {"type": "Point", "coordinates": [-74.0, 40.7]}
        date_range (tuple[datetime, datetime]): Start and end dates for the search.

    Returns:
        pystac.ItemCollection: A collection of STAC items matching the search criteria.
    """
    try:
        # Connect to the STAC catalog
        catalog = Client.open(PLANETARY_COMPUTER_STAC_URL)

        # Format the date range for the search query
        time_range_str = f"{date_range[0].strftime('%Y-%m-%d')}/{date_range[1].strftime('%Y-%m-%d')}"

        # Define the search query
        search = catalog.search(
            collections=["sentinel-2-l2a"],
            intersects=aoi,
            datetime=time_range_str,
            query={"eo:cloud_cover": {"lt": 20}},  # Filter for images with less than 20% cloud cover
        )

        # Get all matched items
        items = search.item_collection()
        print(f"Found {len(items)} items matching the criteria.")
        return items

    except Exception as e:
        print(f"An error occurred during STAC search: {e}")
        return None

