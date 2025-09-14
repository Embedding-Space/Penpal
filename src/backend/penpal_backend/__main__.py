"""Entry point for running the Penpal backend server."""

import os
import uvicorn

if __name__ == "__main__":
    # Use info level to allow Electron to parse startup URL from Uvicorn logs
    # Only enable reload in development
    environment = os.getenv("ENVIRONMENT", "development")
    reload = environment == "development"

    uvicorn.run(
        "penpal_backend.app:create_app",
        host="localhost",
        port=0,
        log_level="info",
        reload=reload,
        factory=True,
    )
