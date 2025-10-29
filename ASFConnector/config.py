"""
Configuration module for ASFConnector using Pydantic.
Reads configuration from .env file with validation.
"""

from pydantic import Field, field_validator, ValidationError
from pydantic_settings import BaseSettings, SettingsConfigDict
from loguru import logger


class ASFConfig(BaseSettings):
    """
    ASF Connection Configuration with Pydantic validation.

    Reads from environment variables or .env file.
    """

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", case_sensitive=False, extra="ignore"
    )

    # ASF IPC settings with defaults
    asf_host: str = Field(default="127.0.0.1", description="ASF IPC host address")

    asf_port: str = Field(default="1242", description="ASF IPC port")

    asf_password: str | None = Field(
        default=None, description="ASF IPC password (optional)"
    )

    asf_path: str = Field(default="/Api", description="ASF IPC API path")

    enable_rich_traceback: bool = Field(
        default=False, description="Enable rich traceback for better error display"
    )

    @field_validator("asf_host")
    @classmethod
    def validate_host(cls, v: str) -> str:
        """Validate host is not empty"""
        if not v or not v.strip():
            raise ValueError("ASF_HOST cannot be empty")
        return v.strip()

    @field_validator("asf_port")
    @classmethod
    def validate_port(cls, v: str) -> str:
        """Validate port is a valid number"""
        v = v.strip()
        try:
            port_num = int(v)
            if not (1 <= port_num <= 65535):
                raise ValueError(f"Port must be between 1 and 65535, got {port_num}")
        except ValueError as e:
            if "invalid literal" in str(e):
                raise ValueError(f'Port must be a valid number, got "{v}"')
            raise
        return v

    @field_validator("asf_path")
    @classmethod
    def validate_path(cls, v: str) -> str:
        """Validate path starts with /"""
        v = v.strip()
        if not v.startswith("/"):
            v = "/" + v
        return v

    def get_connection_params(self) -> dict:
        """
        Get connection parameters as a dictionary for ASFConnector.

        Returns:
            dict: Connection parameters
        """
        params = {
            "host": self.asf_host,
            "port": self.asf_port,
            "path": self.asf_path,
        }

        if self.asf_password:
            params["password"] = self.asf_password

        return params

    def log_config(self) -> None:
        """Log current configuration (without password)"""
        logger.info(
            f"ASF Config - Host: {self.asf_host}, "
            f"Port: {self.asf_port}, "
            f"Path: {self.asf_path}, "
            f"Password: {'***' if self.asf_password else 'None'}"
        )


def load_config() -> ASFConfig:
    """
    Load and validate ASF configuration.

    Returns:
        ASFConfig: Validated configuration object

    Raises:
        ValidationError: If configuration is invalid
    """
    try:
        config = ASFConfig()
        config.log_config()
        return config
    except ValidationError as e:
        logger.error(f"Configuration validation failed: {e}")
        raise


# Create a singleton instance for easy import
try:
    asf_config = load_config()
except ValidationError:
    logger.warning("Failed to load config from .env, using defaults")
    asf_config = ASFConfig()
