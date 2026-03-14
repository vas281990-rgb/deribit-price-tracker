from pydantic import BaseModel
 
class PriceRecordResponse(BaseModel):
    """Schema for serializing price record data in API responses."""
    id: int
    ticker: str
    price: float
    timestamp: int
 
    model_config = {'from_attributes': True}
    # from_attributes=True: allows the schema to interface directly with ORM objects
    # Essential for converting SQLAlchemy models into JSON-compatible formats
