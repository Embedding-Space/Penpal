"""Entry point for running the Penpal backend server."""

import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "penpal_backend.app:create_app",
        host="localhost",
        port=0,
        log_level="info",
        reload=True,
        factory=True,
    )
