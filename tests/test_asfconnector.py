"""
Tests for ASFConnector main class and core functionality.
"""

from unittest.mock import AsyncMock, Mock, patch

import pytest

from ASFConnector import ASFConnector
from ASFConnector.config import ASFConfig
from ASFConnector.error import (
    ASFNetworkError,
)


class TestASFConnectorInitialization:
    """Test ASFConnector initialization and configuration."""

    def test_init_with_direct_parameters(self):
        """Test initialization with direct parameters."""
        connector = ASFConnector(host="192.168.1.100", port="8080", password="test_pass")
        assert connector.host == "192.168.1.100"
        assert connector.port == "8080"
        assert connector.connection_handler is not None

    def test_init_with_config_object(self):
        """Test initialization with ASFConfig object."""
        config = ASFConfig(asf_host="test.example.com", asf_port="9999")
        connector = ASFConnector(config=config)
        assert connector.host == "test.example.com"
        assert connector.port == "9999"

    def test_init_with_defaults(self):
        """Test initialization with default values."""
        connector = ASFConnector()
        assert connector.host == "127.0.0.1"
        assert connector.port == "1242"
        assert connector.path == "/Api"

    def test_from_config_classmethod(self):
        """Test from_config classmethod."""
        config = ASFConfig(asf_host="classmethod.test", asf_port="7777")
        connector = ASFConnector.from_config(config)
        assert connector.host == "classmethod.test"
        assert connector.port == "7777"

    def test_controllers_initialized(self):
        """Test that all controllers are properly initialized."""
        connector = ASFConnector()
        assert connector.asf is not None
        assert connector.bot is not None
        assert connector.command is not None
        assert connector.nlog is not None
        assert connector.type is not None
        assert connector.structure is not None
        assert connector.twofa is not None


class TestASFConnectorContextManager:
    """Test ASFConnector context manager functionality."""

    @pytest.mark.asyncio
    async def test_context_manager_with_mock(self, mock_asf_connector):
        """Test context manager usage with mock."""
        async with mock_asf_connector as connector:
            assert connector is not None
            assert connector.connection_handler._client is not None

    @pytest.mark.asyncio
    async def test_context_manager_health_check(self, monkeypatch):
        """Test that health check is performed on context entry."""
        config = ASFConfig(asf_host="127.0.0.1", asf_port="1242")
        connector = ASFConnector.from_config(config)

        health_check_called = False

        async def mock_health_check():
            nonlocal health_check_called
            health_check_called = True
            return {"Success": True, "Message": "OK"}

        monkeypatch.setattr(connector, "health_check", mock_health_check)

        async with connector as conn:
            assert health_check_called
            assert conn is not None

    @pytest.mark.asyncio
    async def test_context_manager_health_check_failure(self, monkeypatch):
        """Test that health check failure raises exception."""
        config = ASFConfig(asf_host="127.0.0.1", asf_port="1242")
        connector = ASFConnector.from_config(config)

        async def mock_health_check_fail():
            raise ASFNetworkError("Connection failed")

        monkeypatch.setattr(connector, "health_check", mock_health_check_fail)

        with pytest.raises(ASFNetworkError):
            async with connector:
                pass


class TestHealthCheck:
    """Test health check functionality."""

    @pytest.mark.asyncio
    async def test_health_check_success(self, mock_asf_connector, mock_httpx_client):
        """Test successful health check."""
        mock_response = AsyncMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"Success": True, "Message": "OK"}
        mock_response.raise_for_status = Mock()
        mock_httpx_client.get.return_value = mock_response

        mock_asf_connector.connection_handler._client = mock_httpx_client

        result = await mock_asf_connector.health_check()
        assert result["Success"] is True
        assert result["Message"] == "OK"

    @pytest.mark.asyncio
    async def test_health_check_with_text_response(self, mock_asf_connector, mock_httpx_client):
        """Test health check with plain text response."""
        mock_response = AsyncMock()
        mock_response.status_code = 200
        mock_response.json.side_effect = ValueError("Not JSON")
        mock_response.text = "OK"
        mock_response.raise_for_status = Mock()
        mock_httpx_client.get.return_value = mock_response

        mock_asf_connector.connection_handler._client = mock_httpx_client

        result = await mock_asf_connector.health_check()
        assert result["Success"] is True
        assert result["Message"] == "OK"


class TestBackwardCompatibility:
    """Test backward compatibility methods."""

    @pytest.mark.asyncio
    async def test_get_asf_info_backward_compat(self, mock_asf_connector):
        """Test get_asf_info backward compatibility method."""
        mock_response = {
            "Success": True,
            "Result": {"Version": "6.2.2.3", "BuildVariant": "generic"},
        }

        with patch.object(mock_asf_connector.asf, "get_info", return_value=mock_response):
            result = await mock_asf_connector.get_asf_info()
            assert result["Success"] is True
            assert result["Result"]["Version"] == "6.2.2.3"

    @pytest.mark.asyncio
    async def test_get_bot_info_backward_compat(self, mock_asf_connector):
        """Test get_bot_info backward compatibility method."""
        mock_response = {
            "Success": True,
            "Result": {
                "test_bot": {
                    "IsConnectedAndLoggedOn": False,
                    "BotConfig": {"Enabled": True},
                    "CardsFarmer": {"Paused": False},
                }
            },
        }

        with patch.object(mock_asf_connector.bot, "get_info", return_value=mock_response):
            result = await mock_asf_connector.get_bot_info("test_bot")
            assert "Bot test_bot:" in result

    @pytest.mark.asyncio
    async def test_bot_redeem_backward_compat(self, mock_asf_connector):
        """Test bot_redeem backward compatibility method."""
        mock_response = {
            "Success": True,
            "Result": {
                "test_bot": {
                    "KEY1": {
                        "Result": 1,
                        "PurchaseResultDetail": 0,
                    }
                }
            },
        }

        with patch.object(mock_asf_connector.bot, "redeem", return_value=mock_response):
            result = await mock_asf_connector.bot_redeem("test_bot", "KEY1")
            assert "test_bot" in result

    @pytest.mark.asyncio
    async def test_send_command_backward_compat(self, mock_asf_connector):
        """Test send_command backward compatibility method."""
        mock_response = {"Success": True, "Result": "Command executed"}

        with patch.object(mock_asf_connector.command, "execute", return_value=mock_response):
            result = await mock_asf_connector.send_command("status ASF")
            assert "Command executed" in result


class TestErrorModule:
    """Test error module accessibility."""

    def test_error_module_accessible(self):
        """Test that error module is accessible from connector."""
        connector = ASFConnector()
        assert connector.error is not None
        assert hasattr(connector.error, "ASFConnectorError")
        assert hasattr(connector.error, "ASFHTTPError")
        assert hasattr(connector.error, "ASFNetworkError")


class TestConnectionPoolReuse:
    """Test connection pool reuse functionality."""

    @pytest.mark.asyncio
    async def test_connection_pool_created(self, mock_asf_connector):
        """Test that connection pool is created in context manager."""
        async with mock_asf_connector as connector:
            assert connector.connection_handler._client is not None

    @pytest.mark.asyncio
    async def test_connection_pool_closed(self, mock_asf_connector):
        """Test that connection pool is properly closed."""
        async with mock_asf_connector as connector:
            client = connector.connection_handler._client
            assert client is not None

        # After exiting context, client should be closed
        assert mock_asf_connector.connection_handler._client is None


class TestASFConnectorIntegration:
    """Integration tests for ASFConnector (with mocks)."""

    @pytest.mark.asyncio
    async def test_full_workflow_with_context_manager(self, mock_asf_connector):
        """Test full workflow using context manager."""
        mock_asf_response = {"Success": True, "Result": {"Version": "6.2.2.3"}}
        mock_bot_response = {"Success": True, "Result": {"test_bot": {}}}

        with patch.object(mock_asf_connector.asf, "get_info", return_value=mock_asf_response):
            with patch.object(mock_asf_connector.bot, "get_info", return_value=mock_bot_response):
                async with mock_asf_connector as connector:
                    # Get ASF info
                    asf_info = await connector.asf.get_info()
                    assert asf_info["Success"] is True

                    # Get bot info
                    bot_info = await connector.bot.get_info("test_bot")
                    assert bot_info["Success"] is True
