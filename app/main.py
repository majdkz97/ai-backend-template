from fastapi import FastAPI, HTTPException, Depends
from sqlmodel import Session, select
from loguru import logger
from .settings import settings
from .database import engine, get_session, create_db_and_tables
from .models import Item
from .schemas import ItemCreate, ItemResponse
from uuid import uuid4
from datetime import datetime

logger.add("app.log", rotation="500 MB", level="INFO")

app = FastAPI(
    title="Majd's AI Backend Template",
    description="Reusable FastAPI + Postgres template",
    version="0.1.0",
)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()
    logger.info("Database tables created")

@app.get("/")
def read_root():
    logger.info("Root endpoint accessed")
    return {"message": "AI Backend Template is live with PostgreSQL!"}

@app.get("/health", response_model=dict)
def health_check():
    logger.debug("Health check performed")
    return {"status": "healthy"}

@app.post("/items/", response_model=ItemResponse)
def create_item(item: ItemCreate, session: Session = Depends(get_session)):
    db_item = Item(**item.dict())
    session.add(db_item)
    session.commit()
    session.refresh(db_item)
    logger.info(f"Item created: {db_item.id}")
    return db_item

@app.get("/items/", response_model=list[ItemResponse])
def read_items(session: Session = Depends(get_session)):
    items = session.exec(select(Item)).all()
    return items

@app.get("/items/{item_id}", response_model=ItemResponse)
def read_item(item_id: str, session: Session = Depends(get_session)):
    item = session.get(Item, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item