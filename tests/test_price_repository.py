import pytest
from unittest.mock import AsyncMock, MagicMock
from app.repositories.price_repository import PriceRepository
from app.database.models import PriceRecord
 
@pytest.mark.asyncio
async def test_get_latest_returns_none_when_no_data(mock_session):
    """Test: Returns None when no data exists for the given ticker."""
    mock_result = MagicMock()
    # Mocking the call chain: execute() -> scalars() -> first() -> None
    mock_result.scalars.return_value.first.return_value = None
    mock_session.execute = AsyncMock(return_value=mock_result)
 
    repo = PriceRepository(mock_session)
    result = await repo.get_latest('btc_usd')
 
    assert result is None
 
@pytest.mark.asyncio
async def test_get_latest_returns_correct_record(mock_session):
    """Test: Returns the correct record when data is present."""
    expected = PriceRecord(ticker='btc_usd', price=65000.0, timestamp=1700000000)
    mock_result = MagicMock()
    # Mocking the call chain to return the expected PriceRecord object
    mock_result.scalars.return_value.first.return_value = expected
    mock_session.execute = AsyncMock(return_value=mock_result)
 
    repo = PriceRepository(mock_session)
    result = await repo.get_latest('btc_usd')
 
    assert result == expected
    assert result.price == 65000.0
 
@pytest.mark.asyncio
async def test_get_all_by_ticker_returns_list(mock_session):
    """Test: Returns a list of all records for a specific ticker."""
    records = [
        PriceRecord(ticker='eth_usd', price=3000.0, timestamp=1700000060),
        PriceRecord(ticker='eth_usd', price=2990.0, timestamp=1700000000),
    ]
    mock_result = MagicMock()
    # Mocking the call chain: execute() -> scalars() -> all() -> list of records
    mock_result.scalars.return_value.all.return_value = records
    mock_session.execute = AsyncMock(return_value=mock_result)
 
    repo = PriceRepository(mock_session)
    result = await repo.get_all_by_ticker('eth_usd')
 
    assert len(result) == 2
    assert result[0].price == 3000.0