from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.api.routers.prices import router as prices_router
from app.database.connection import engine
from app.database.models import Base
 
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Everything before yield runs on startup
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Everything after yield runs on shutdown (can leave empty)

app = FastAPI(
    title='Deribit Price Tracker',
    description='API for tracking cryptocurrency prices from the Deribit exchange',
    version='1.0.0',
    lifespan=lifespan,
    # Metadata will be displayed in the Swagger UI at /docs or /redoc.
)
 
# Include the router to activate all endpoints defined in prices.py.
app.include_router(prices_router)