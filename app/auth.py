from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from loguru import logger
from .settings import settings


class ApiKeyMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Allow public access to docs, schema, health checks, and root
        if request.url.path in ["/", "/health", "/docs", "/redoc", "/openapi.json"]:
            return await call_next(request)

        api_key = request.headers.get("X-API-Key")
        if not api_key or api_key != settings.API_KEY:
            logger.warning(f"Unauthorized access attempt: {request.url.path}")
            return JSONResponse(
                status_code=401,
                content={"detail": "Invalid or missing API Key"},
            )

        response = await call_next(request)
        return response

