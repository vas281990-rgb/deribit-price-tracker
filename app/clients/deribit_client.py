import aiohttp
from typing import Optional
from app.config import settings
 
class DeribitClient:
    """Async HTTP client for interacting with the Deribit API."""
 
    def __init__(self):
        self._base_url = settings.DERIBIT_BASE_URL
        self._session: Optional[aiohttp.ClientSession] = None
        # Persistent session to leverage connection pooling; avoid re-creating sessions per request.
 
    async def __aenter__(self):
        # Enables 'async with' usage; ensures proper resource initialization.
        self._session = aiohttp.ClientSession()
        return self
 
    async def __aexit__(self, *args):
        # Gracefully closes the session and releases connections even if an error occurs.
        if self._session:
            await self._session.close()
 
    async def get_index_price(self, ticker: str) -> float:
        """Fetches the index price for a specific ticker (e.g., 'btc_usd')."""
        url = f'{self._base_url}/public/get_index_price'
        params = {'index_name': ticker}
 
        async with self._session.get(url, params=params) as response:
            # Validates HTTP status; raises an exception for 4xx/5xx responses.
            response.raise_for_status()
            
            # Non-blocking JSON parsing.
            data = await response.json()
            
            # Standard Deribit API response structure.
            return data['result']['index_price']