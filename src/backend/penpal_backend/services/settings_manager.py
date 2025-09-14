"""Settings management for the Penpal backend."""

import os
from pathlib import Path

from dotenv import load_dotenv


class SettingsManager:
    """Singleton settings manager for the Penpal backend."""
    
    _instance = None
    _initialized = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not self._initialized:
            self._load_settings()
            self._initialized = True
    
    def _load_settings(self) -> None:
        """Load environment variables from .env file."""
        # Load from project root .env file
        project_root = Path(__file__).parent.parent.parent.parent.parent
        env_file = project_root / ".env"
        
        if env_file.exists():
            load_dotenv(env_file)
    
    @property
    def logfire_token(self) -> str | None:
        """Get the Logfire token from environment variables."""
        return os.getenv("LOGFIRE_TOKEN")
    
    @property
    def service_name(self) -> str:
        """Get the service name for Logfire."""
        return "penpal-backend"
    
    @property
    def service_version(self) -> str:
        """Get the service version for Logfire."""
        return "1.0.0"


# Convenience function for easy access
def get_settings() -> SettingsManager:
    """Get the settings manager instance."""
    return SettingsManager()
