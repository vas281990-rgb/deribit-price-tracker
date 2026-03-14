import asyncio
import time
from app.tasks.celery_app import celery_app
from app.clients.deribit_client import DeribitClient
from app.database.connection import AsyncSessionLocal
from app.repositories.price_repository import PriceRepository
 
# List of assets to track. Using a constant makes it easy to add new tickers.
TICKERS = ['btc_usd', 'eth_usd']
 
@celery_app.task(name='app.tasks.price_tasks.fetch_and_save_prices')
def fetch_and_save_prices():
    """
    Entry point for Celery. 
    Since Celery workers are synchronous by default, asyncio.run() 
    is used to execute the asynchronous logic.
    """
    asyncio.run(_fetch_and_save())
 
async def _fetch_and_save():
    """
    Core logic: fetches prices from API and persists them to the database.
    Separating the sync wrapper from async logic improves maintainability.
    """
    async with DeribitClient() as client:
        async with AsyncSessionLocal() as session:
            repo = PriceRepository(session)
            
            # Using a single timestamp for all tickers ensures data consistency for the snapshot.
            current_timestamp = int(time.time())
 
            for ticker in TICKERS:
                price = await client.get_index_price(ticker)
                await repo.create(
                    ticker=ticker,
                    price=price,
                    timestamp=current_timestamp,
                )
 
            # Atomic operation: commit once to save all records or roll back on error.
            await session.commit()
            