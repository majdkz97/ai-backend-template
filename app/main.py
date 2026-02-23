from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from loguru import logger
from .settings import settings

logger.add("app.log", rotation="500 MB", level="INFO")

app = FastAPI(
    title="Majd's AI Backend Template",
    description="Reusable FastAPI + Postgres template for AI projects",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

@app.get("/")
def read_root():
    logger.info("Root endpoint accessed")
    return {"message": "AI Backend Template is live!"}

@app.get("/health", status_code=status.HTTP_200_OK)
def health_check():
    logger.debug("Health check performed")
    return JSONResponse({"status": "healthy"})