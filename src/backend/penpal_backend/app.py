"""FastAPI application factory."""

from contextlib import asynccontextmanager

import logfire
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from penpal_backend.api import health
from penpal_backend.services.settings_manager import get_settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handle application lifespan events."""
    # Startup
    logfire.info("Penpal backend starting up")
    yield
    # Shutdown
    logfire.info("Penpal backend shutting down")


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    # Get settings (automatically loads environment config)
    settings = get_settings()
    
    # Initialize Logfire
    logfire.configure(
        token=settings.logfire_token,
        service_name=settings.service_name,
        service_version=settings.service_version,
    )
    logfire.info("Logfire initialized successfully")
    
    app = FastAPI(
        title="Penpal Backend",
        description="Backend API for Penpal AI agent management platform",
        version="1.0.0",
        lifespan=lifespan,
    )

    # Configure CORS for Electron frontend
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:*", "http://127.0.0.1:*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include API routers
    app.include_router(health.router, prefix="/api")

    return app
