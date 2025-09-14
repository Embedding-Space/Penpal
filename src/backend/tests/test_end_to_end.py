"""End-to-end tests for Logfire instrumentation."""

import os
from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from penpal_backend.app import create_app


def test_end_to_end_with_real_logfire_token():
    """Test end-to-end flow with a real Logfire token (mocked)."""
    # Simulate having a real Logfire token
    real_token = "pylf_v1_us_test123456789"
    
    with patch.dict(os.environ, {"LOGFIRE_TOKEN": real_token}):
        with patch("penpal_backend.app.logfire.configure") as mock_configure:
            with patch("penpal_backend.app.logfire.info") as mock_info:
                app = create_app()
                
                # Test complete application lifecycle
                with TestClient(app) as client:
                    # Test health endpoint
                    health_response = client.get("/api/health")
                    assert health_response.status_code == 200
                    assert health_response.json() == {
                        "status": "healthy",
                        "service": "penpal-backend"
                    }
                
                # Verify complete Logfire setup
                mock_configure.assert_called_once_with(
                    token=real_token,
                    service_name="penpal-backend",
                    service_version="1.0.0",
                )
                
                # Verify all lifecycle events were logged
                all_calls = [str(call) for call in mock_info.call_args_list]
                assert any("Logfire initialized successfully" in call for call in all_calls)
                assert any("Penpal backend starting up" in call for call in all_calls)
                assert any("Penpal backend shutting down" in call for call in all_calls)


def test_end_to_end_without_logfire_token():
    """Test end-to-end flow without Logfire token."""
    with patch.dict(os.environ, {}, clear=True):
        with patch("penpal_backend.services.settings_manager.SettingsManager") as mock_settings_class:
            mock_settings = mock_settings_class.return_value
            mock_settings.logfire_token = None
            mock_settings.service_name = "penpal-backend"
            mock_settings.service_version = "1.0.0"
            
            with patch("penpal_backend.app.logfire.configure") as mock_configure:
                with patch("penpal_backend.app.logfire.info") as mock_info:
                    app = create_app()
                    
                    # Test complete application lifecycle
                    with TestClient(app) as client:
                        # Test health endpoint
                        health_response = client.get("/api/health")
                        assert health_response.status_code == 200
                        assert health_response.json() == {
                            "status": "healthy",
                            "service": "penpal-backend"
                        }
                    
                    # Verify Logfire was still configured (with None token)
                    mock_configure.assert_called_once_with(
                        token=None,
                        service_name="penpal-backend",
                        service_version="1.0.0",
                    )
                    
                    # Verify all lifecycle events were logged
                    all_calls = [str(call) for call in mock_info.call_args_list]
                    assert any("Logfire initialized successfully" in call for call in all_calls)
                    assert any("Penpal backend starting up" in call for call in all_calls)
                    assert any("Penpal backend shutting down" in call for call in all_calls)


def test_end_to_end_settings_manager_integration():
    """Test end-to-end integration with SettingsManager."""
    with patch.dict(os.environ, {"LOGFIRE_TOKEN": "test-token-789"}):
        with patch("penpal_backend.app.logfire.configure") as mock_configure:
            with patch("penpal_backend.app.logfire.info") as mock_info:
                app = create_app()
                
                # Test that SettingsManager is properly integrated
                with TestClient(app) as client:
                    response = client.get("/api/health")
                    assert response.status_code == 200
                
                # Verify SettingsManager provided correct values
                mock_configure.assert_called_once()
                call_args = mock_configure.call_args
                
                # These values come from SettingsManager
                assert call_args.kwargs["service_name"] == "penpal-backend"
                assert call_args.kwargs["service_version"] == "1.0.0"
                assert call_args.kwargs["token"] == "test-token-789"


def test_end_to_end_fastapi_lifespan_integration():
    """Test end-to-end integration with FastAPI lifespan events."""
    with patch.dict(os.environ, {"LOGFIRE_TOKEN": "test-token"}):
        with patch("penpal_backend.app.logfire.configure"):
            with patch("penpal_backend.app.logfire.info") as mock_info:
                app = create_app()
                
                # Test that lifespan events work correctly
                with TestClient(app) as client:
                    # Make multiple requests to test lifespan
                    for i in range(2):
                        response = client.get("/api/health")
                        assert response.status_code == 200
                
                # Verify lifespan events were called in correct order
                all_calls = mock_info.call_args_list
                
                # Find startup and shutdown calls
                startup_call = None
                shutdown_call = None
                
                for call in all_calls:
                    if "starting up" in str(call):
                        startup_call = call
                    elif "shutting down" in str(call):
                        shutdown_call = call
                
                # Both should exist
                assert startup_call is not None
                assert shutdown_call is not None
                
                # Startup should come before shutdown
                startup_index = all_calls.index(startup_call)
                shutdown_index = all_calls.index(shutdown_call)
                assert startup_index < shutdown_index


def test_end_to_end_cors_integration():
    """Test end-to-end integration with CORS middleware."""
    with patch.dict(os.environ, {"LOGFIRE_TOKEN": "test-token"}):
        with patch("penpal_backend.app.logfire.configure"):
            app = create_app()
            
            # Test that CORS middleware doesn't interfere with Logfire
            with TestClient(app) as client:
                # Test regular GET request
                response = client.get("/api/health")
                # Should work fine with CORS middleware present
                assert response.status_code == 200
                assert response.json() == {
                    "status": "healthy",
                    "service": "penpal-backend"
                }
