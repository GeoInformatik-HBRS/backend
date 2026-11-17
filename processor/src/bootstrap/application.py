import os
import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.health import router as health_router
from src.api.reports import router as reports_router

# Local Vite dev server (frontend default port 5173). Override with a
# comma-separated CORS_ORIGINS environment variable.
DEFAULT_CORS_ORIGINS = "http://localhost:5173,http://127.0.0.1:5173"


def create_app() -> FastAPI:
    logging.basicConfig(level=logging.INFO)
    app = FastAPI()
    app.add_middleware(
        CORSMiddleware,
        allow_origins=_cors_origins(),
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(health_router)
    app.include_router(reports_router)
    return app


def _cors_origins() -> list[str]:
    value = os.environ.get("CORS_ORIGINS", DEFAULT_CORS_ORIGINS)
    return [origin.strip() for origin in value.split(",") if origin.strip()]
