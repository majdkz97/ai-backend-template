from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ItemCreate(BaseModel):
    name: str
    description: Optional[str] = None
    category: str
    price: float

class ItemResponse(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    category: str
    price: float
    created_at: datetime