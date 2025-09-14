"""Tests for the SettingsManager class."""

import os
from unittest.mock import patch

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
    assert settings.service_version == "1.0.0"


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
    """Test settings manager loads from .env file."""
    # Clear the singleton
    SettingsManager._instance = None
    SettingsManager._initialized = False
    
    with patch("penpal_backend.services.settings_manager.Path") as mock_path_class:
        mock_path_instance = mock_path_class.return_value
        mock_env_file = mock_path_instance.parent.parent.parent.parent.parent.__truediv__.return_value
        mock_env_file.exists.return_value = True
        
        with patch("penpal_backend.services.settings_manager.load_dotenv") as mock_load_dotenv:
            settings = SettingsManager()
            mock_load_dotenv.assert_called_once_with(mock_env_file)


def test_settings_manager_without_env_file():
    """Test settings manager handles missing .env file gracefully."""
    # Clear the singleton
    SettingsManager._instance = None
    SettingsManager._initialized = False
    
    with patch("penpal_backend.services.settings_manager.Path") as mock_path_class:
        mock_path_instance = mock_path_class.return_value
        mock_env_file = mock_path_instance.parent.parent.parent.parent.parent.__truediv__.return_value
        mock_env_file.exists.return_value = False
        
        with patch("penpal_backend.services.settings_manager.load_dotenv") as mock_load_dotenv:
            settings = SettingsManager()
            mock_load_dotenv.assert_not_called()
