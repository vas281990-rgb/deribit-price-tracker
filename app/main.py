from fastapi import FastAPI
from app.api.routes.prices import router as prices_router
from app.database.connection import engine
from app.database.models import Base
 
app = FastAPI(
    title='Deribit Price Tracker',
    description='API for tracking cryptocurrency prices from the Deribit exchange',
    version='1.0.0',
    # Metadata will be displayed in the Swagger UI at /docs or /redoc.
)
 
@app.on_event('startup')
async def startup():
    """Executes once when the server starts."""
    async with engine.begin() as conn:
        # Create tables if they do not exist; skip if they already are in the DB.
        # This is a safe way to ensure the schema is ready for work.
        await conn.run_sync(Base.metadata.create_all)
 
# Include the router to activate all endpoints defined in prices.py.
app.include_router(prices_router)