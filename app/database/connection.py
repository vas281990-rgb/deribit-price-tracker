from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from app.config import settings

# Database engine configuration 
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=False,
   
    pool_size=10,
    max_overflow=20,
   
)

# Session factory for handling async database transactions
AsyncSessionLocal = async_sessionmaker(
    engine,
    expire_on_commit=False,

)

# Dependency for FastAPI endpoints 
async def get_db():
    """Dependency Injection для FastAPI."""

    async with AsyncSessionLocal() as session:
        yield session
  
