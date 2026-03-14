from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from app.database.models import PriceRecord
 
class PriceRepository:
    def __init__(self, session: AsyncSession):
        self._session = session
        # Dependency Injection: session is provided from outside.
        # This makes it easy to swap the real DB with a mock session for unit testing.
 
    async def create(self, ticker: str, price: float, timestamp: int) -> PriceRecord:
        record = PriceRecord(ticker=ticker, price=price, timestamp=timestamp)
        self._session.add(record)
        # add() marks the object for insertion; it hasn't hit the database yet.
        
        await self._session.flush()
        # flush() pushes SQL to the DB without committing the transaction.
        # This allows us to access the database-generated ID immediately.
        return record
 
    async def get_all_by_ticker(self, ticker: str) -> list[PriceRecord]:
        """Retrieves all records for a ticker, ordered from newest to oldest."""
        query = (
            select(PriceRecord)
            .where(PriceRecord.ticker == ticker)
            .order_by(desc(PriceRecord.timestamp))
        )
        result = await self._session.execute(query)
        return result.scalars().all()
        # scalars() extracts the model objects instead of raw result tuples.
 
    async def get_latest(self, ticker: str) -> PriceRecord | None:
        """Fetches the most recent price record based on the maximum timestamp."""
        query = (
            select(PriceRecord)
            .where(PriceRecord.ticker == ticker)
            .order_by(desc(PriceRecord.timestamp))
            .limit(1)
            # Using limit(1) is more efficient than fetching all and taking the first index.
        )
        result = await self._session.execute(query)
        return result.scalars().first()
        # first() safely returns None if no records match the criteria.
 
    async def get_by_date_range(
        self, ticker: str, date_from: int, date_to: int
    ) -> list[PriceRecord]:
        """Filters price history within a specific UNIX timestamp range."""
        query = (
            select(PriceRecord)
            .where(
                PriceRecord.ticker == ticker,
                PriceRecord.timestamp >= date_from,
                PriceRecord.timestamp <= date_to,
            )
            .order_by(desc(PriceRecord.timestamp))
        )
        result = await self._session.execute(query)
        return result.scalars().all()