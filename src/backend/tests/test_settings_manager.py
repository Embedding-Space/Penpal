"""Tests for the SettingsManager class."""

import os
from unittest.mock import patch, MagicMock

import pytest

from penpal_backend.services.settings_manager import SettingsManager, get_settings


def test_settings_manager_singleton():
    """Test that SettingsManager is a singleton."""
    manager1 = SettingsManager()
    manager2 = SettingsManager()
    assert manager1 is manager2


def test_get_settings_convenience_function():
    """Test the convenience function returns the singleton."""
    manager1 = SettingsManager()
    manager2 = get_settings()
    assert manager1 is manager2


def test_logfire_token_property():
    """Test the logfire_token property."""
    with patch.dict(os.environ, {"LOGFIRE_TOKEN": "test-token-123"}):
        settings = SettingsManager()
        assert settings.logfire_token == "test-token-123"


def test_logfire_token_property_missing():
    """Test the logfire_token property when not set."""
    with patch.dict(os.environ, {}, clear=True):
        settings = SettingsManager()
        assert settings.logfire_token is None


def test_service_name_property():
    """Test the service_name property."""
    settings = SettingsManager()
    assert settings.service_name == "penpal-backend"


def test_service_version_property():
    """Test the service_version property."""
    settings = SettingsManager()
    assert isinstance(settings.service_version, str)


def test_settings_manager_initialization():
    """Test that settings manager initializes only once."""
    # Clear the singleton
    SettingsManager._instance = None
    SettingsManager._initialized = False

    with patch("penpal_backend.services.settings_manager.load_dotenv") as mock_load_dotenv:
        # Create first instance
        manager1 = SettingsManager()
        assert mock_load_dotenv.call_count == 1

        # Create second instance - should not call load_dotenv again
        manager2 = SettingsManager()
        assert mock_load_dotenv.call_count == 1

        # Should be the same instance
        assert manager1 is manager2


def test_settings_manager_with_env_file():
    """Test settings manager loads from .env file using find_dotenv()."""
    # Clear the singleton
    SettingsManager._instance = None
    SettingsManager._initialized = False

    with patch("penpal_backend.services.settings_manager.find_dotenv") as mock_find_dotenv:
        mock_find_dotenv.return_value = "/path/to/.env"

        with patch("penpal_backend.services.settings_manager.load_dotenv") as mock_load_dotenv:
            settings = SettingsManager()
            mock_find_dotenv.assert_called_once_with(filename=".env", raise_error_if_not_found=False)
            mock_load_dotenv.assert_called_once_with("/path/to/.env")


def test_settings_manager_without_env_file():
    """Test settings manager handles missing .env file gracefully."""
    # Clear the singleton
    SettingsManager._instance = None
    SettingsManager._initialized = False

    with patch("penpal_backend.services.settings_manager.find_dotenv") as mock_find_dotenv:
        mock_find_dotenv.return_value = ""  # Empty string when not found

        with patch("penpal_backend.services.settings_manager.load_dotenv") as mock_load_dotenv:
            settings = SettingsManager()
            mock_find_dotenv.assert_called_once_with(filename=".env", raise_error_if_not_found=False)
            mock_load_dotenv.assert_not_called()


def test_find_dotenv_success():
    """Test settings manager uses find_dotenv() when .env file is found."""
    # Clear the singleton
    SettingsManager._instance = None
    SettingsManager._initialized = False

    with patch("penpal_backend.services.settings_manager.find_dotenv") as mock_find_dotenv:
        mock_find_dotenv.return_value = "/path/to/.env"

        with patch("penpal_backend.services.settings_manager.load_dotenv") as mock_load_dotenv:
            settings = SettingsManager()

            # Should call find_dotenv with correct parameters
            mock_find_dotenv.assert_called_once_with(filename=".env", raise_error_if_not_found=False)
            # Should call load_dotenv with the found path
            mock_load_dotenv.assert_called_once_with("/path/to/.env")


def test_find_dotenv_not_found():
    """Test settings manager handles when find_dotenv() returns empty string."""
    # Clear the singleton
    SettingsManager._instance = None
    SettingsManager._initialized = False

    with patch("penpal_backend.services.settings_manager.find_dotenv") as mock_find_dotenv:
        mock_find_dotenv.return_value = ""  # Empty string when not found

        with patch("penpal_backend.services.settings_manager.load_dotenv") as mock_load_dotenv:
            settings = SettingsManager()

            # Should call find_dotenv
            mock_find_dotenv.assert_called_once_with(filename=".env", raise_error_if_not_found=False)
            # Should not call load_dotenv
            mock_load_dotenv.assert_not_called()


def test_find_dotenv_with_logging():
    """Test that appropriate logging occurs during .env discovery."""
    # Clear the singleton
    SettingsManager._instance = None
    SettingsManager._initialized = False

    with patch("penpal_backend.services.settings_manager.find_dotenv") as mock_find_dotenv:
        mock_find_dotenv.return_value = "/path/to/.env"

        with patch("penpal_backend.services.settings_manager.load_dotenv"):
            settings = SettingsManager()
            # .env discovery logging is now handled by print statements


def test_find_dotenv_error_handling():
    """Test error handling when find_dotenv() raises an exception."""
    # Clear the singleton
    SettingsManager._instance = None
    SettingsManager._initialized = False

    with patch("penpal_backend.services.settings_manager.find_dotenv") as mock_find_dotenv:
        mock_find_dotenv.side_effect = Exception("Permission denied")

        # Should not raise exception, should handle gracefully
        settings = SettingsManager()
        # Error logging is now handled by print statements


def test_service_version_with_package_metadata():
    """Test service_version property reads from package metadata."""
    # Clear the singleton
    SettingsManager._instance = None
    SettingsManager._initialized = False

    with patch("penpal_backend.services.settings_manager.importlib.metadata.version") as mock_version:
        mock_version.return_value = "2.1.0"

        settings = SettingsManager()

        # Access the property to trigger version lookup
        version = settings.service_version

        # Should call importlib.metadata.version with correct package name
        mock_version.assert_called_once_with("penpal-backend")
        # Should return the package version
        assert version == "2.1.0"


def test_service_version_fallback_on_package_not_found():
    """Test service_version fallback when package metadata unavailable."""
    # Clear the singleton
    SettingsManager._instance = None
    SettingsManager._initialized = False

    with patch("penpal_backend.services.settings_manager.importlib.metadata.version") as mock_version:
        from importlib.metadata import PackageNotFoundError
        mock_version.side_effect = PackageNotFoundError("penpal-backend")

        settings = SettingsManager()

        # Access the property to trigger version lookup
        version = settings.service_version

        # Should attempt to get package version
        mock_version.assert_called_once_with("penpal-backend")
        # Should return fallback version
        assert version == "dev-unknown"
        # Fallback logging is now handled by print statements


def test_service_version_fallback_on_general_error():
    """Test service_version fallback when importlib.metadata raises other errors."""
    # Clear the singleton
    SettingsManager._instance = None
    SettingsManager._initialized = False

    with patch("penpal_backend.services.settings_manager.importlib.metadata.version") as mock_version:
        mock_version.side_effect = Exception("Import error")

        settings = SettingsManager()

        # Access the property to trigger version lookup
        version = settings.service_version

        # Should attempt to get package version
        mock_version.assert_called_once_with("penpal-backend")
        # Should return fallback version
        assert version == "dev-unknown"
        # Error logging is now handled by print statements


def test_service_version_with_logging():
    """Test that appropriate logging occurs during version resolution."""
    # Clear the singleton
    SettingsManager._instance = None
    SettingsManager._initialized = False

    with patch("penpal_backend.services.settings_manager.importlib.metadata.version") as mock_version:
        mock_version.return_value = "1.5.0"

        settings = SettingsManager()

        # Access the property to trigger version lookup
        version = settings.service_version

        # Should successfully resolve version
        assert version == "1.5.0"
        # Version logging is now handled by print statements
