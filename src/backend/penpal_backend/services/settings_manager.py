"""Settings management for the Penpal backend."""

import importlib.metadata
import os
from pathlib import Path

from dotenv import load_dotenv, find_dotenv


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
        try:
            env_file_path = find_dotenv(filename=".env", raise_error_if_not_found=False)

            if env_file_path:
                print(f"[SettingsManager] Found .env file: {env_file_path}")
                load_dotenv(env_file_path)
            else:
                print("[SettingsManager] No .env file found. Using system environment variables only.")
        except Exception as e:
            print(f"[SettingsManager] Error loading .env file: {e}")
            print("[SettingsManager] Continuing with system environment variables only.")

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
        try:
            version = importlib.metadata.version("penpal-backend")
            print(f"[SettingsManager] Retrieved service version: {version}")
            return version
        except importlib.metadata.PackageNotFoundError:
            print("[SettingsManager] Package 'penpal-backend' not found in metadata. Using fallback version: dev-unknown")
            return "dev-unknown"
        except Exception as e:
            print(f"[SettingsManager] Error retrieving package version: {e}. Using fallback: dev-unknown")
            return "dev-unknown"


# Convenience function for easy access
def get_settings() -> SettingsManager:
    """Get the settings manager instance."""
    return SettingsManager()
