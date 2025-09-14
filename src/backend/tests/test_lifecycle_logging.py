"""Tests for application lifecycle logging."""

import os
from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from penpal_backend.app import create_app


def test_startup_logging():
    """Test that startup logging occurs when app starts."""
    with patch.dict(os.environ, {"LOGFIRE_TOKEN": "test-token"}):
        with patch("penpal_backend.app.logfire.configure"):
            with patch("penpal_backend.app.logfire.info") as mock_info:
                app = create_app()
                
                # Create client to trigger startup
                with TestClient(app) as client:
                    response = client.get("/api/health")
                    assert response.status_code == 200
                
                # Verify startup log was called
                startup_calls = [call for call in mock_info.call_args_list 
                               if "starting up" in str(call)]
                assert len(startup_calls) == 1


def test_shutdown_logging():
    """Test that shutdown logging occurs when app shuts down."""
    with patch.dict(os.environ, {"LOGFIRE_TOKEN": "test-token"}):
        with patch("penpal_backend.app.logfire.configure"):
            with patch("penpal_backend.app.logfire.info") as mock_info:
                app = create_app()
                
                # Create client and trigger shutdown
                with TestClient(app) as client:
                    response = client.get("/api/health")
                    assert response.status_code == 200
                
                # Verify shutdown log was called (happens when client context exits)
                shutdown_calls = [call for call in mock_info.call_args_list 
                                if "shutting down" in str(call)]
                assert len(shutdown_calls) == 1


def test_lifecycle_logging_without_token():
    """Test lifecycle logging works even without Logfire token."""
    with patch.dict(os.environ, {}, clear=True):
        with patch("penpal_backend.services.settings_manager.SettingsManager") as mock_settings_class:
            mock_settings = mock_settings_class.return_value
            mock_settings.logfire_token = None
            mock_settings.service_name = "penpal-backend"
            mock_settings.service_version = "1.0.0"
            
            with patch("penpal_backend.app.logfire.configure"):
                with patch("penpal_backend.app.logfire.info") as mock_info:
                    app = create_app()
                    
                    # Create client to trigger lifecycle events
                    with TestClient(app) as client:
                        response = client.get("/api/health")
                        assert response.status_code == 200
                    
                    # Verify both startup and shutdown logs were called
                    startup_calls = [call for call in mock_info.call_args_list 
                                   if "starting up" in str(call)]
                    shutdown_calls = [call for call in mock_info.call_args_list 
                                     if "shutting down" in str(call)]
                    
                    assert len(startup_calls) == 1
                    assert len(shutdown_calls) == 1


def test_lifecycle_logging_message_content():
    """Test that lifecycle logging messages have correct content."""
    with patch.dict(os.environ, {"LOGFIRE_TOKEN": "test-token"}):
        with patch("penpal_backend.app.logfire.configure"):
            with patch("penpal_backend.app.logfire.info") as mock_info:
                app = create_app()
                
                # Create client to trigger lifecycle events
                with TestClient(app) as client:
                    response = client.get("/api/health")
                    assert response.status_code == 200
                
                # Check that the correct messages were logged
                all_calls = [str(call) for call in mock_info.call_args_list]
                
                assert any("Penpal backend starting up" in call for call in all_calls)
                assert any("Penpal backend shutting down" in call for call in all_calls)


def test_lifecycle_logging_timing():
    """Test that startup happens before shutdown."""
    with patch.dict(os.environ, {"LOGFIRE_TOKEN": "test-token"}):
        with patch("penpal_backend.app.logfire.configure"):
            with patch("penpal_backend.app.logfire.info") as mock_info:
                app = create_app()
                
                # Create client to trigger lifecycle events
                with TestClient(app) as client:
                    response = client.get("/api/health")
                    assert response.status_code == 200
                
                # Verify startup was called before shutdown
                all_calls = mock_info.call_args_list
                startup_index = None
                shutdown_index = None
                
                for i, call in enumerate(all_calls):
                    if "starting up" in str(call):
                        startup_index = i
                    elif "shutting down" in str(call):
                        shutdown_index = i
                
                assert startup_index is not None
                assert shutdown_index is not None
                assert startup_index < shutdown_index
