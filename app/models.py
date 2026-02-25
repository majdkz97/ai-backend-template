from uuid import uuid4
from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class Item(SQLModel, table=True):
    id: Optional[str] = Field(default_factory=lambda: str(uuid4()), primary_key=True)
    name: str
    description: Optional[str] = None
    category: str
    price: float
    created_at: datetime = Field(default_factory=datetime.now)