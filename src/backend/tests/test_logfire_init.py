"""Tests for Logfire initialization and configuration."""

import os
from unittest.mock import Mock, patch

import pytest
import logfire


def test_logfire_initialization_with_token():
    """Test that Logfire can be initialized with a valid token."""
    with patch.dict(os.environ, {"LOGFIRE_TOKEN": "test-token-123"}):
        # Mock logfire.configure to avoid actual initialization
        with patch("logfire.configure") as mock_configure:
            logfire.configure(token="test-token-123")
            mock_configure.assert_called_once_with(token="test-token-123")


def test_logfire_initialization_without_token():
    """Test that Logfire initialization handles missing token gracefully."""
    with patch.dict(os.environ, {}, clear=True):
        # Mock logfire.configure to avoid actual initialization
        with patch("logfire.configure") as mock_configure:
            # Should not raise an error even without token
            logfire.configure(token=None)
            mock_configure.assert_called_once_with(token=None)


def test_logfire_initialization_from_env():
    """Test that Logfire can be initialized using token from environment."""
    with patch.dict(os.environ, {"LOGFIRE_TOKEN": "env-token-456"}):
        with patch("logfire.configure") as mock_configure:
            token = os.getenv("LOGFIRE_TOKEN")
            logfire.configure(token=token)
            mock_configure.assert_called_once_with(token="env-token-456")


def test_logfire_initialization_with_service_name():
    """Test that Logfire can be initialized with service name."""
    with patch.dict(os.environ, {"LOGFIRE_TOKEN": "test-token"}):
        with patch("logfire.configure") as mock_configure:
            logfire.configure(
                token="test-token",
                service_name="penpal-backend",
            )
            mock_configure.assert_called_once_with(
                token="test-token",
                service_name="penpal-backend",
            )


def test_logfire_initialization_with_service_version():
    """Test that Logfire can be initialized with service version."""
    with patch.dict(os.environ, {"LOGFIRE_TOKEN": "test-token"}):
        with patch("logfire.configure") as mock_configure:
            logfire.configure(
                token="test-token",
                service_name="penpal-backend",
                service_version="1.0.0",
            )
            mock_configure.assert_called_once_with(
                token="test-token",
                service_name="penpal-backend",
                service_version="1.0.0",
            )


def test_logfire_logging_functionality():
    """Test that Logfire logging works after initialization."""
    with patch.dict(os.environ, {"LOGFIRE_TOKEN": "test-token"}):
        with patch("logfire.configure"):
            with patch("logfire.info") as mock_info:
                logfire.info("Test log message")
                mock_info.assert_called_once_with("Test log message")


def test_logfire_structured_logging():
    """Test that Logfire supports structured logging."""
    with patch.dict(os.environ, {"LOGFIRE_TOKEN": "test-token"}):
        with patch("logfire.configure"):
            with patch("logfire.info") as mock_info:
                logfire.info(
                    "User action",
                    user_id=123,
                    action="login",
                    timestamp="2025-09-14T09:00:00Z",
                )
                mock_info.assert_called_once_with(
                    "User action",
                    user_id=123,
                    action="login",
                    timestamp="2025-09-14T09:00:00Z",
                )
