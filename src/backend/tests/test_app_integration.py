"""Tests for FastAPI app integration with Logfire."""

import os
from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from penpal_backend.app import create_app
from penpal_backend.services.settings_manager import SettingsManager


def test_app_creation_with_logfire_token():
    """Test app creation with Logfire token."""
    with patch.dict(os.environ, {"LOGFIRE_TOKEN": "test-token-123"}):
        with patch("penpal_backend.app.logfire.configure") as mock_configure:
            with patch("penpal_backend.app.logfire.info") as mock_info:
                app = create_app()
                
                # Verify Logfire was configured
                mock_configure.assert_called_once_with(
                    token="test-token-123",
                    service_name="penpal-backend",
                    service_version="1.0.0",
                )
                
                # Verify startup log
                mock_info.assert_called_with("Logfire initialized successfully")
                
                # Verify app was created
                assert app is not None
                assert app.title == "Penpal Backend"


def test_app_creation_without_logfire_token():
    """Test app creation without Logfire token."""
    with patch.dict(os.environ, {}, clear=True):
        with patch("penpal_backend.services.settings_manager.SettingsManager") as mock_settings_class:
            mock_settings = mock_settings_class.return_value
            mock_settings.logfire_token = None
            mock_settings.service_name = "penpal-backend"
            mock_settings.service_version = "1.0.0"
            
            with patch("penpal_backend.app.logfire.configure") as mock_configure:
                with patch("penpal_backend.app.logfire.info") as mock_info:
                    app = create_app()
                    
                    # Verify Logfire was configured with None token
                    mock_configure.assert_called_once_with(
                        token=None,
                        service_name="penpal-backend",
                        service_version="1.0.0",
                    )
                    
                    # Verify startup log
                    mock_info.assert_called_with("Logfire initialized successfully")
                    
                    # Verify app was created
                    assert app is not None
                    assert app.title == "Penpal Backend"


def test_app_startup_event():
    """Test app startup event logging."""
    with patch.dict(os.environ, {"LOGFIRE_TOKEN": "test-token"}):
        with patch("penpal_backend.app.logfire.configure"):
            with patch("penpal_backend.app.logfire.info") as mock_info:
                app = create_app()
                
                # Trigger startup event
                with TestClient(app) as client:
                    # Make a request to trigger startup
                    response = client.get("/api/health")
                    assert response.status_code == 200
                
                # Verify startup log was called
                assert mock_info.call_count >= 2  # At least init + startup


def test_app_shutdown_event():
    """Test app shutdown event logging."""
    with patch.dict(os.environ, {"LOGFIRE_TOKEN": "test-token"}):
        with patch("penpal_backend.app.logfire.configure"):
            with patch("penpal_backend.app.logfire.info") as mock_info:
                app = create_app()
                
                # Create client and trigger shutdown
                with TestClient(app) as client:
                    response = client.get("/api/health")
                    assert response.status_code == 200
                
                # Verify shutdown log was called (this happens when client context exits)
                assert mock_info.call_count >= 2  # At least init + shutdown


def test_app_health_endpoint():
    """Test that health endpoint works with Logfire integration."""
    with patch.dict(os.environ, {"LOGFIRE_TOKEN": "test-token"}):
        with patch("penpal_backend.app.logfire.configure"):
            app = create_app()
            
            with TestClient(app) as client:
                response = client.get("/api/health")
                assert response.status_code == 200
                assert response.json() == {"status": "healthy", "service": "penpal-backend"}
