from fastapi import FastAPI, HTTPException
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from fastapi.openapi.utils import get_openapi
from loguru import logger
import sys

from .api import api_router
from .core import ApiKeyMiddleware, create_db_and_tables

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
app.include_router(api_router)


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

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    logger.error(f"HTTP error {exc.status_code}: {exc.detail} - {request.url}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )