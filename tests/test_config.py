"""
Tests for ASFConnector configuration management.
"""

from pydantic import ValidationError
import pytest

from ASFConnector.config import ASFConfig


class TestASFConfig:
    """Test ASFConfig class and validation."""

    def test_default_config(self, monkeypatch, tmp_path):
        """Test default configuration values."""
        # Create a temporary directory without .env file
        monkeypatch.chdir(tmp_path)

        # Clear environment variables to test defaults
        monkeypatch.delenv("ASF_HOST", raising=False)
        monkeypatch.delenv("ASF_PORT", raising=False)
        monkeypatch.delenv("ASF_PASSWORD", raising=False)
        monkeypatch.delenv("ASF_PATH", raising=False)
        monkeypatch.delenv("ENABLE_RICH_TRACEBACK", raising=False)

        config = ASFConfig()
        assert config.asf_host == "127.0.0.1"
        assert config.asf_port == "1242"
        assert config.asf_password is None
        assert config.asf_path == "/Api"
        assert config.enable_rich_traceback is False

    def test_custom_config(self):
        """Test custom configuration values."""
        config = ASFConfig(
            asf_host="192.168.1.100",
            asf_port="8080",
            asf_password="my_password",
            asf_path="/CustomApi",
        )
        assert config.asf_host == "192.168.1.100"
        assert config.asf_port == "8080"
        assert config.asf_password == "my_password"
        assert config.asf_path == "/CustomApi"

    def test_path_validation_adds_slash(self):
        """Test that path validation adds leading slash if missing."""
        config = ASFConfig(asf_path="Api")
        assert config.asf_path == "/Api"

    def test_path_validation_preserves_slash(self):
        """Test that path validation preserves existing leading slash."""
        config = ASFConfig(asf_path="/Api")
        assert config.asf_path == "/Api"

    def test_host_validation_strips_whitespace(self):
        """Test that host validation strips whitespace."""
        config = ASFConfig(asf_host="  127.0.0.1  ")
        assert config.asf_host == "127.0.0.1"

    def test_host_validation_rejects_empty(self):
        """Test that host validation rejects empty strings."""
        with pytest.raises(ValidationError) as exc_info:
            ASFConfig(asf_host="")
        assert "ASF_HOST cannot be empty" in str(exc_info.value)

    def test_port_validation_valid_range(self):
        """Test that port validation accepts valid port numbers."""
        config = ASFConfig(asf_port="1")
        assert config.asf_port == "1"

        config = ASFConfig(asf_port="65535")
        assert config.asf_port == "65535"

        config = ASFConfig(asf_port="8080")
        assert config.asf_port == "8080"

    def test_port_validation_rejects_out_of_range(self):
        """Test that port validation rejects out of range ports."""
        with pytest.raises(ValidationError) as exc_info:
            ASFConfig(asf_port="0")
        assert "Port must be between 1 and 65535" in str(exc_info.value)

        with pytest.raises(ValidationError) as exc_info:
            ASFConfig(asf_port="65536")
        assert "Port must be between 1 and 65535" in str(exc_info.value)

    def test_port_validation_rejects_invalid(self):
        """Test that port validation rejects non-numeric ports."""
        with pytest.raises(ValidationError) as exc_info:
            ASFConfig(asf_port="abc")
        assert "Port must be a valid number" in str(exc_info.value)

    def test_get_connection_params(self):
        """Test get_connection_params method."""
        config = ASFConfig(
            asf_host="192.168.1.100",
            asf_port="8080",
            asf_password="my_password",
            asf_path="/CustomApi",
        )
        params = config.get_connection_params()
        assert params["host"] == "192.168.1.100"
        assert params["port"] == "8080"
        assert params["password"] == "my_password"
        assert params["path"] == "/CustomApi"

    def test_get_connection_params_no_password(self, monkeypatch):
        """Test get_connection_params without password."""
        # Clear password from environment
        monkeypatch.delenv("ASF_PASSWORD", raising=False)

        config = ASFConfig(asf_host="127.0.0.1", asf_port="1242", asf_password=None)
        params = config.get_connection_params()
        assert "password" not in params

    def test_log_config(self):
        """Test log_config method."""
        from loguru import logger

        # Capture log output
        log_output = []

        def log_sink(message):
            log_output.append(message)

        # Remove existing handlers and add our capture handler
        logger.remove()
        logger.add(log_sink, level="DEBUG")

        config = ASFConfig(asf_password="secret", asf_host="test.example.com")
        config.log_config()

        # Check that logs were captured
        assert len(log_output) > 0
        log_text = "".join(log_output)

        # Password should be masked in logs
        assert "***" in log_text
        assert "secret" not in log_text
        assert "test.example.com" in log_text

    def test_load_config_from_env(self, monkeypatch):
        """Test loading config from environment variables."""
        monkeypatch.setenv("ASF_HOST", "test.example.com")
        monkeypatch.setenv("ASF_PORT", "9999")
        monkeypatch.setenv("ASF_PASSWORD", "test_pass")

        config = ASFConfig()
        assert config.asf_host == "test.example.com"
        assert config.asf_port == "9999"
        assert config.asf_password == "test_pass"

    def test_case_insensitive_env_vars(self, monkeypatch):
        """Test that environment variables are case insensitive."""
        monkeypatch.setenv("asf_host", "lowercase.example.com")
        monkeypatch.setenv("ASF_PORT", "7777")

        config = ASFConfig()
        assert config.asf_host == "lowercase.example.com"
        assert config.asf_port == "7777"

    def test_extra_fields_ignored(self):
        """Test that extra fields in config are ignored."""
        # This should not raise an error
        config = ASFConfig(
            asf_host="127.0.0.1",
            extra_field="ignored",  # type: ignore
            another_extra="also_ignored",  # type: ignore
        )
        assert config.asf_host == "127.0.0.1"
        assert not hasattr(config, "extra_field")

    def test_enable_rich_traceback_flag(self):
        """Test enable_rich_traceback configuration."""
        config = ASFConfig(enable_rich_traceback=True)
        assert config.enable_rich_traceback is True

        config = ASFConfig(enable_rich_traceback=False)
        assert config.enable_rich_traceback is False
