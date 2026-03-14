from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.connection import get_db
from app.repositories.price_repository import PriceRepository
from app.schemas.price_schemas import PriceRecordResponse
 
router = APIRouter(prefix='/prices', tags=['prices'])
# prefix='/prices': All routes within this router start with /prices.
# tags=['prices']: Groups these endpoints in the Swagger UI (/docs) for better organization.
 
# ENDPOINT 1: GET /prices/
@router.get('/', response_model=list[PriceRecordResponse])
async def get_all_prices(
    ticker: str = Query(...),
    # Query(...) makes this a required query parameter (Ellipsis means no default value).
    # Requests without a ticker will automatically return 422 Unprocessable Entity.
    db: AsyncSession = Depends(get_db),
    # Dependency Injection: FastAPI provides the database session automatically.
):
    repo = PriceRepository(db)
    return await repo.get_all_by_ticker(ticker)
 
# ENDPOINT 2: GET /prices/latest
@router.get('/latest', response_model=PriceRecordResponse)
async def get_latest_price(
    ticker: str = Query(...),
    db: AsyncSession = Depends(get_db),
):
    repo = PriceRepository(db)
    record = await repo.get_latest(ticker)
    if record is None:
        # Returns a 404 status code if the ticker data is missing.
        raise HTTPException(
            status_code=404,
            detail=f'No data for ticker: {ticker}',
        )
    return record
 
# ENDPOINT 3: GET /prices/filter
@router.get('/filter', response_model=list[PriceRecordResponse])
async def get_prices_by_date(
    ticker: str = Query(...),
    date_from: int = Query(..., description='Start UNIX timestamp'),
    date_to: int = Query(..., description='End UNIX timestamp'),
    db: AsyncSession = Depends(get_db),
):
    repo = PriceRepository(db)
    return await repo.get_by_date_range(ticker, date_from, date_to)