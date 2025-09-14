"""Integration tests for complete Logfire flow."""

import os
from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from penpal_backend.app import create_app


def test_complete_logfire_integration_with_token():
    """Test complete Logfire integration flow with token."""
    with patch.dict(os.environ, {"LOGFIRE_TOKEN": "test-token-123"}):
        with patch("penpal_backend.app.logfire.configure") as mock_configure:
            with patch("penpal_backend.app.logfire.info") as mock_info:
                app = create_app()
                
                # Test complete flow: startup -> request -> shutdown
                with TestClient(app) as client:
                    # Make multiple requests to test logging
                    response1 = client.get("/api/health")
                    assert response1.status_code == 200
                    
                    response2 = client.get("/api/health")
                    assert response2.status_code == 200
                
                # Verify Logfire was configured correctly
                mock_configure.assert_called_once_with(
                    token="test-token-123",
                    service_name="penpal-backend",
                    service_version="1.0.0",
                )
                
                # Verify all expected logs were called
                all_calls = [str(call) for call in mock_info.call_args_list]
                
                # Should have initialization, startup, and shutdown logs
                assert any("Logfire initialized successfully" in call for call in all_calls)
                assert any("Penpal backend starting up" in call for call in all_calls)
                assert any("Penpal backend shutting down" in call for call in all_calls)


def test_complete_logfire_integration_without_token():
    """Test complete Logfire integration flow without token."""
    with patch.dict(os.environ, {}, clear=True):
        with patch("penpal_backend.services.settings_manager.SettingsManager") as mock_settings_class:
            mock_settings = mock_settings_class.return_value
            mock_settings.logfire_token = None
            mock_settings.service_name = "penpal-backend"
            mock_settings.service_version = "1.0.0"
            
            with patch("penpal_backend.app.logfire.configure") as mock_configure:
                with patch("penpal_backend.app.logfire.info") as mock_info:
                    app = create_app()
                    
                    # Test complete flow: startup -> request -> shutdown
                    with TestClient(app) as client:
                        response = client.get("/api/health")
                        assert response.status_code == 200
                    
                    # Verify Logfire was configured with None token
                    mock_configure.assert_called_once_with(
                        token=None,
                        service_name="penpal-backend",
                        service_version="1.0.0",
                    )
                    
                    # Verify all expected logs were called
                    all_calls = [str(call) for call in mock_info.call_args_list]
                    
                    # Should have initialization, startup, and shutdown logs
                    assert any("Logfire initialized successfully" in call for call in all_calls)
                    assert any("Penpal backend starting up" in call for call in all_calls)
                    assert any("Penpal backend shutting down" in call for call in all_calls)


def test_logfire_integration_with_environment_loading():
    """Test that Logfire integration works with environment variable loading."""
    # Create a temporary environment setup
    with patch.dict(os.environ, {"LOGFIRE_TOKEN": "env-token-456"}):
        with patch("penpal_backend.app.logfire.configure") as mock_configure:
            with patch("penpal_backend.app.logfire.info") as mock_info:
                app = create_app()
                
                # Test that environment variables are properly loaded
                with TestClient(app) as client:
                    response = client.get("/api/health")
                    assert response.status_code == 200
                
                # Verify token was loaded from environment
                mock_configure.assert_called_once_with(
                    token="env-token-456",
                    service_name="penpal-backend",
                    service_version="1.0.0",
                )


def test_logfire_integration_service_metadata():
    """Test that Logfire integration includes correct service metadata."""
    with patch.dict(os.environ, {"LOGFIRE_TOKEN": "test-token"}):
        with patch("penpal_backend.app.logfire.configure") as mock_configure:
            app = create_app()
            
            # Verify service metadata is correct
            mock_configure.assert_called_once()
            call_args = mock_configure.call_args
            
            assert call_args.kwargs["service_name"] == "penpal-backend"
            assert call_args.kwargs["service_version"] == "1.0.0"
            assert call_args.kwargs["token"] == "test-token"


def test_logfire_integration_multiple_requests():
    """Test that Logfire integration handles multiple requests correctly."""
    with patch.dict(os.environ, {"LOGFIRE_TOKEN": "test-token"}):
        with patch("penpal_backend.app.logfire.configure"):
            with patch("penpal_backend.app.logfire.info") as mock_info:
                app = create_app()
                
                # Test multiple requests in same session
                with TestClient(app) as client:
                    for i in range(3):
                        response = client.get("/api/health")
                        assert response.status_code == 200
                
                # Should only have one startup and one shutdown log
                startup_calls = [call for call in mock_info.call_args_list 
                               if "starting up" in str(call)]
                shutdown_calls = [call for call in mock_info.call_args_list 
                                 if "shutting down" in str(call)]
                
                assert len(startup_calls) == 1
                assert len(shutdown_calls) == 1


def test_logfire_integration_error_handling():
    """Test that Logfire integration handles errors gracefully."""
    with patch.dict(os.environ, {"LOGFIRE_TOKEN": "test-token"}):
        with patch("penpal_backend.app.logfire.configure"):
            with patch("penpal_backend.app.logfire.info") as mock_info:
                app = create_app()
                
                # Test that app still works even if Logfire has issues
                with TestClient(app) as client:
                    # Make a request to non-existent endpoint
                    response = client.get("/api/nonexistent")
                    assert response.status_code == 404
                
                # App should still log lifecycle events
                all_calls = [str(call) for call in mock_info.call_args_list]
                assert any("Penpal backend starting up" in call for call in all_calls)
                assert any("Penpal backend shutting down" in call for call in all_calls)
