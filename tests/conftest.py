"""
Pytest configuration and fixtures for ASFConnector tests.
"""

import os
from unittest.mock import AsyncMock, Mock

import httpx
import pytest
from pytest_asyncio import fixture

# 设置测试环境
os.environ["ENVIRONMENT"] = "test"


@fixture(scope="session")
def mock_asf_config():
    """Provide mock ASF configuration for tests."""
    return {
        "asf_host": "127.0.0.1",
        "asf_port": "1242",
        "asf_password": "test_password",
        "asf_path": "/Api",
        "enable_rich_traceback": False,
    }


@fixture(scope="session")
def mock_asf_responses():
    """Provide mock ASF API responses for tests."""
    return {
        "asf_info": {
            "Success": True,
            "Result": {
                "Version": "6.2.2.3",
                "BuildVariant": "generic",
                "GlobalConfig": {},
                "Memory": 0,
                "ProcessStartTime": "2024-01-01T00:00:00Z",
            },
        },
        "bot_info": {
            "Success": True,
            "Result": {
                "test_bot": {
                    "BotName": "test_bot",
                    "IsConnectedAndLoggedOn": True,
                    "CardsFarmer": {
                        "Paused": False,
                        "CurrentGamesFarming": [],
                        "GamesToFarm": [],
                        "TimeRemaining": "00:00:00",
                    },
                    "BotConfig": {"Enabled": True},
                }
            },
        },
        "health_check": {"Success": True, "Message": "OK"},
        "generic_success": {"Success": True, "Message": "OK"},
        "generic_error": {"Success": False, "Message": "Error occurred"},
    }


@fixture
async def mock_httpx_client(mock_asf_responses):
    """Provide a mock httpx.AsyncClient for testing."""
    mock_client = AsyncMock(spec=httpx.AsyncClient)

    # Configure default successful responses
    mock_response = AsyncMock(spec=httpx.Response)
    mock_response.status_code = 200
    mock_response.json.return_value = mock_asf_responses["generic_success"]
    mock_response.text = "OK"
    mock_response.raise_for_status = Mock()

    mock_client.get.return_value = mock_response
    mock_client.post.return_value = mock_response
    mock_client.delete.return_value = mock_response
    mock_client.aclose = AsyncMock()

    return mock_client


@fixture
def mock_ipc_handler(mock_httpx_client, mock_asf_config):
    """Provide a mock IPCProtocolHandler for testing."""
    from ASFConnector.IPCProtocol import IPCProtocolHandler

    handler = IPCProtocolHandler(
        host=mock_asf_config["asf_host"],
        port=mock_asf_config["asf_port"],
        path=mock_asf_config["asf_path"],
        password=mock_asf_config["asf_password"],
    )
    handler._client = mock_httpx_client
    return handler


@fixture
async def mock_asf_connector(mock_asf_config, monkeypatch):
    """Provide a mock ASFConnector for testing without real network calls."""
    from ASFConnector import ASFConnector
    from ASFConnector.config import ASFConfig

    # Create config
    config = ASFConfig(**mock_asf_config)

    # Create connector with mock
    connector = ASFConnector.from_config(config)

    # Mock the health check to avoid real network calls
    async def mock_health_check():
        return {"Success": True, "Message": "OK"}

    monkeypatch.setattr(connector, "health_check", mock_health_check)

    yield connector

    # Cleanup
    if connector.connection_handler._client:
        await connector.connection_handler._client.aclose()


@fixture
def mock_env_file(tmp_path, mock_asf_config):
    """Create a temporary .env file for testing."""
    env_file = tmp_path / ".env"
    env_content = f"""
ASF_HOST={mock_asf_config["asf_host"]}
ASF_PORT={mock_asf_config["asf_port"]}
ASF_PASSWORD={mock_asf_config["asf_password"]}
ASF_PATH={mock_asf_config["asf_path"]}
ENABLE_RICH_TRACEBACK={str(mock_asf_config["enable_rich_traceback"]).lower()}
"""
    env_file.write_text(env_content)
    return env_file


@pytest.fixture(autouse=True)
def isolate_environment(monkeypatch):
    """Isolate test environment from .env file and system environment variables."""
    # Clear ASF-related environment variables for clean testing
    for env_var in ["ASF_HOST", "ASF_PORT", "ASF_PASSWORD", "ASF_PATH", "ENABLE_RICH_TRACEBACK"]:
        monkeypatch.delenv(env_var, raising=False)
    return


@pytest.fixture(autouse=True)
def reset_loguru():
    """Reset loguru handlers before each test to avoid log pollution."""
    from loguru import logger

    logger.remove()
    # Add a simple handler for tests
    logger.add(
        lambda msg: None,  # Silent handler
        level="DEBUG",
    )
    yield
    logger.remove()


def pytest_collection_modifyitems(items: list[pytest.Item]):
    """Automatically mark async tests with session scope."""
    from pytest_asyncio import is_async_test

    pytest_asyncio_tests = (item for item in items if is_async_test(item))
    session_scope_marker = pytest.mark.asyncio(loop_scope="session")
    for async_test in pytest_asyncio_tests:
        async_test.add_marker(session_scope_marker, append=False)
