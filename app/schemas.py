from pydantic import BaseModel
from typing import Optional

class ItemCreate(BaseModel):
    name: str
    description: Optional[str] = None
    category: str

class ItemResponse(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    category: str