from sqlalchemy import Column, Integer, String, Float, BigInteger
from sqlalchemy.orm import DeclarativeBase
 
class Base(DeclarativeBase):
    """Base class for all models; used by SQLAlchemy to track table metadata."""
    pass
 
class PriceRecord(Base):
    """Model to store historical ticker prices from the exchange."""
    __tablename__ = 'price_records'
 
    # Primary key with auto-increment handled by the DB (e.g., PostgreSQL)
    id = Column(Integer, primary_key=True, autoincrement=True)

    # Ticker symbol (e.g., 'btc_usd'). Indexed for faster WHERE filtering.
    ticker = Column(String(20), nullable=False, index=True)

    # Current asset price. Float is sufficient for crypto price precision.
    price = Column(Float, nullable=False)
    
    # UNIX timestamp. BigInteger is used to avoid the Y2K38 overflow problem.
    # Indexed to optimize time-series queries and sorting.
    timestamp = Column(BigInteger, nullable=False, index=True)
