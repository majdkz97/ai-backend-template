from fastapi import FastAPI, HTTPException, Depends
from sqlmodel import Session, select
from loguru import logger
from .settings import settings
from .database import engine, get_session, create_db_and_tables
from .models import Item
from .schemas import ItemCreate, ItemResponse
from uuid import uuid4
from datetime import datetime
import sys
from fastapi.responses import JSONResponse
from fastapi.requests import Request
from fastapi.openapi.utils import get_openapi
from .auth import ApiKeyMiddleware

logger.remove()  # Remove default handler
logger.add(
    "logs/app.log",
    rotation="500 MB",      # Rotate when file reaches 500 MB
    retention="10 days",    # Keep logs for 10 days
    level="INFO",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message} | {extra}"
)
logger.add(
    sys.stdout,
    level="DEBUG",          # Show DEBUG in console during dev
    format="{time} | {level} | {message}"
)

app = FastAPI(
    title="Majd's AI Backend Template",
    description="Reusable FastAPI + Postgres template",
    version="0.1.0",
)
app.add_middleware(ApiKeyMiddleware)


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )
    security_schemes = openapi_schema.setdefault("components", {}).setdefault(
        "securitySchemes", {}
    )
    security_schemes["ApiKeyAuth"] = {
        "type": "apiKey",
        "in": "header",
        "name": "X-API-Key",
    }
    for path in openapi_schema.get("paths", {}).values():
        for method in path.values():
            method.setdefault("security", []).append({"ApiKeyAuth": []})
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi  # type: ignore[assignment]

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

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    logger.error(f"HTTP error {exc.status_code}: {exc.detail} - {request.url}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )