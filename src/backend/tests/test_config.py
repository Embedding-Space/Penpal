"""Tests for environment configuration and Logfire setup."""

import os
import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest
from dotenv import load_dotenv


def test_load_logfire_token_from_env():
    """Test that LOGFIRE_TOKEN can be loaded from environment variables."""
    # Test with environment variable
    with patch.dict(os.environ, {"LOGFIRE_TOKEN": "test-token-123"}):
        load_dotenv()
        token = os.getenv("LOGFIRE_TOKEN")
        assert token == "test-token-123"


def test_load_logfire_token_from_dotenv_file():
    """Test that LOGFIRE_TOKEN can be loaded from .env file."""
    # Create temporary .env file
    with tempfile.NamedTemporaryFile(mode="w", suffix=".env", delete=False) as f:
        f.write("LOGFIRE_TOKEN=test-token-from-file\n")
        env_file = f.name
    
    try:
        # Load from the temporary .env file
        load_dotenv(env_file)
        token = os.getenv("LOGFIRE_TOKEN")
        assert token == "test-token-from-file"
    finally:
        # Clean up
        os.unlink(env_file)


def test_logfire_token_priority():
    """Test that environment variable takes priority over .env file."""
    # Create temporary .env file
    with tempfile.NamedTemporaryFile(mode="w", suffix=".env", delete=False) as f:
        f.write("LOGFIRE_TOKEN=token-from-file\n")
        env_file = f.name
    
    try:
        # Set environment variable and load .env file
        with patch.dict(os.environ, {"LOGFIRE_TOKEN": "token-from-env"}):
            load_dotenv(env_file)
            token = os.getenv("LOGFIRE_TOKEN")
            assert token == "token-from-env"
    finally:
        # Clean up
        os.unlink(env_file)


def test_missing_logfire_token():
    """Test behavior when LOGFIRE_TOKEN is not set."""
    # Clear the environment variable and don't load .env file
    with patch.dict(os.environ, {}, clear=True):
        # Don't call load_dotenv() to avoid loading existing .env file
        token = os.getenv("LOGFIRE_TOKEN")
        assert token is None


def test_logfire_token_type():
    """Test that LOGFIRE_TOKEN is returned as string."""
    with patch.dict(os.environ, {"LOGFIRE_TOKEN": "test-token"}):
        load_dotenv()
        token = os.getenv("LOGFIRE_TOKEN")
        assert isinstance(token, str)
        assert token == "test-token"
