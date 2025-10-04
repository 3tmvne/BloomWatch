from pystac_client import Client
from datetime import datetime
from pystac.item import Item # Import Item

# URL for the Microsoft Planetary Computer STAC API
PLANETARY_COMPUTER_STAC_URL = "https://planetarycomputer.microsoft.com/api/stac/v1"
SENTINEL_COLLECTION = "sentinel-2-l2a"

def search_sentinel2_data(aoi: dict, date_range: tuple[datetime, datetime]):
    """
    Searches the Planetary Computer for Sentinel-2 L2A data.
    """
    try:
        catalog = Client.open(PLANETARY_COMPUTER_STAC_URL)
        time_range_str = f"{date_range[0].strftime('%Y-%m-%d')}/{date_range[1].strftime('%Y-%m-%d')}"
        search = catalog.search(
            collections=[SENTINEL_COLLECTION],
            intersects=aoi,
            datetime=time_range_str,
            query={"eo:cloud_cover": {"lt": 20}},
        )
        items = search.item_collection()
        print(f"Found {len(items)} items matching the criteria.")
        return items
    except Exception as e:
        print(f"An error occurred during STAC search: {e}")
        return None

# --- NEW FUNCTION ---
def get_item_by_id(item_id: str) -> Item | None:
    """
    Fetches a single STAC item from the Planetary Computer by its ID.
    """
    try:
        catalog = Client.open(PLANETARY_COMPUTER_STAC_URL)
        # The get_item method requires the collection ID and item ID
        item = catalog.get_collection(SENTINEL_COLLECTION).get_item(item_id)
        return item
    except Exception as e:
        # This can happen if the item ID is invalid or not found
        print(f"Could not fetch item '{item_id}'. Error: {e}")
        return None
