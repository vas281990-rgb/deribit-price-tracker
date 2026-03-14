import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch
from app.main import app
from app.database.models import PriceRecord
 
client = TestClient(app)
# TestClient: FastAPI's built-in tool for integration testing.
# It simulates HTTP requests to the app without needing a live server.
 
def test_get_latest_missing_ticker():
    """Test: Missing the required 'ticker' query parameter returns 422 Unprocessable Entity."""
    response = client.get('/prices/latest')
    assert response.status_code == 422
    # FastAPI automatically validates parameters and handles 422 errors.
 
def test_get_latest_not_found():
    """Test: Ticker is provided but no data exists in the repository; returns 404."""
    with patch(
        'app.api.routes.prices.PriceRepository.get_latest',
        new_callable=AsyncMock,
        return_value=None,
    ):
        response = client.get('/prices/latest?ticker=btc_usd')
        assert response.status_code == 404
        # Ensures our HTTPException(status_code=404) logic works correctly.