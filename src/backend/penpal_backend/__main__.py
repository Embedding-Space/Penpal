"""Entry point for running the Penpal backend server."""

import os
import uvicorn

if __name__ == "__main__":
    # Use warning level to suppress Uvicorn INFO messages that clutter Logfire
    # Only enable reload in development
    environment = os.getenv("ENVIRONMENT", "development")
    reload = environment == "development"
    
    uvicorn.run(
        "penpal_backend.app:create_app",
        host="localhost",
        port=0,
        log_level="warning",
        reload=reload,
        factory=True,
    )
