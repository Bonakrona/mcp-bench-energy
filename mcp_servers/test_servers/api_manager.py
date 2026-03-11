"""API manager functions for making requests to OpenDataSoft APIs."""

import logging
from typing import Any
import httpx
from config.config_loader import Settings
from dotenv import load_dotenv

load_dotenv()
# Constants
USER_AGENT = "request-data-retrieval/1.0"
API_BASE = "https://ukpowernetworks.opendatasoft.com/api/explore/v2.1/catalog/datasets"

class APIError(Exception):
    """Custom exception for API errors."""
    def __init__(self, message: str, url: str | None = None):
        self.message = message
        self.url = url
        super().__init__(self.message)


def handle_api_exception(e: Exception, url: str) -> str:
    """ Centralized error handler for API exceptions."""
    if isinstance(e, httpx.HTTPStatusError):
        error_msg = f"HTTP error {e.response.status_code} for {url}: {e}\nResponse content: {e.response.text}"
    elif isinstance(e, httpx.RequestError):
        error_msg = f"Request error for {url}: {e}"
    elif isinstance(e, AttributeError):
        error_msg = f"Attribute error for {url}: {e} - Response may be None or invalid format"
    elif isinstance(e, (ValueError, KeyError, TypeError)):
        error_msg = f"Unexpected error for {url}: {e}"
    else:
        error_msg = f"Unknown error for {url}: {type(e).__name__}: {e}"
    logging.error(error_msg)
    return error_msg

async def make_request_uk_powernetworks(dataset: str, params: dict[str, Any]) -> str | None:
    """Fetch records for a dataset from UK Power Networks OpenDataSoft."""
    settings = Settings()
    api_key = settings.uk_powernetworks_api_key
    if not api_key:
        logging.error("UK POWERNETWORKS api key not found in environment variables.")
        return None
    
    params = dict(params)
    params["apikey"] = api_key

    url = f"{API_BASE}/{dataset}/records"
    headers = {"accept": "application/json; charset=utf-8", "User-Agent": USER_AGENT}
    
    async with httpx.AsyncClient(verify=False) as client:
        try:
            resp = await client.get(url, headers=headers, params=params, timeout=30.0)
            resp.raise_for_status()
            data = resp.json()
        except (httpx.HTTPStatusError, httpx.RequestError, ValueError, KeyError, TypeError, AttributeError) as e:
            return handle_api_exception(e, url)

        if data is None:
            return "Failed to retrieve data from OpenDataSoft API."
        results = data.get("results")
        if not results:
            return "No results found."
        return str(results)