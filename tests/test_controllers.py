"""
Tests for ASFConnector Controller classes.
"""

from unittest.mock import patch

import pytest

from ASFConnector.Controllers.ASFController import ASFController
from ASFConnector.Controllers.BotController import BotController
from ASFConnector.Controllers.CommandController import CommandController
from ASFConnector.Controllers.NLogController import NLogController
from ASFConnector.Controllers.StructureController import StructureController
from ASFConnector.Controllers.TypeController import TypeController


class TestASFController:
    """Test ASFController methods."""

    @pytest.mark.asyncio
    async def test_get_info(self, mock_ipc_handler):
        """Test get_info method."""
        controller = ASFController(mock_ipc_handler)
        mock_response = {"Success": True, "Result": {"Version": "6.2.2.3"}}

        with patch.object(mock_ipc_handler, "get", return_value=mock_response) as mock_get:
            result = await controller.get_info()
            assert result["Success"] is True
            assert result["Result"]["Version"] == "6.2.2.3"
            mock_get.assert_called_once_with("/ASF", None)

    @pytest.mark.asyncio
    async def test_update_config(self, mock_ipc_handler):
        """Test update_config method."""
        controller = ASFController(mock_ipc_handler)
        config = {"AutoRestart": True, "UpdatePeriod": 24}
        mock_response = {"Success": True, "Message": "Config updated"}

        with patch.object(mock_ipc_handler, "post", return_value=mock_response) as mock_post:
            result = await controller.update_config(config)
            assert result["Success"] is True
            mock_post.assert_called_once_with("/ASF", config)

    @pytest.mark.asyncio
    async def test_exit(self, mock_ipc_handler):
        """Test exit method."""
        controller = ASFController(mock_ipc_handler)
        mock_response = {"Success": True, "Message": "ASF is shutting down"}

        with patch.object(mock_ipc_handler, "post", return_value=mock_response) as mock_post:
            result = await controller.exit()
            assert result["Success"] is True
            mock_post.assert_called_once_with("/ASF/Exit", None)

    @pytest.mark.asyncio
    async def test_restart(self, mock_ipc_handler):
        """Test restart method."""
        controller = ASFController(mock_ipc_handler)
        mock_response = {"Success": True, "Message": "ASF is restarting"}

        with patch.object(mock_ipc_handler, "post", return_value=mock_response) as mock_post:
            result = await controller.restart()
            assert result["Success"] is True
            mock_post.assert_called_once_with("/ASF/Restart", None)


class TestBotController:
    """Test BotController methods."""

    @pytest.mark.asyncio
    async def test_get_info_single_bot(self, mock_ipc_handler):
        """Test get_info for single bot."""
        controller = BotController(mock_ipc_handler)
        mock_response = {
            "Success": True,
            "Result": {"test_bot": {"IsConnectedAndLoggedOn": True}},
        }

        with patch.object(mock_ipc_handler, "get", return_value=mock_response) as mock_get:
            result = await controller.get_info("test_bot")
            assert result["Success"] is True
            mock_get.assert_called_once_with("/Bot/test_bot", None)

    @pytest.mark.asyncio
    async def test_get_info_multiple_bots(self, mock_ipc_handler):
        """Test get_info for multiple bots."""
        controller = BotController(mock_ipc_handler)
        mock_response = {
            "Success": True,
            "Result": {
                "bot1": {"IsConnectedAndLoggedOn": True},
                "bot2": {"IsConnectedAndLoggedOn": False},
            },
        }

        with patch.object(mock_ipc_handler, "get", return_value=mock_response) as mock_get:
            result = await controller.get_info("bot1,bot2")
            assert result["Success"] is True
            mock_get.assert_called_once_with("/Bot/bot1,bot2", None)

    @pytest.mark.asyncio
    async def test_get_info_all_bots(self, mock_ipc_handler):
        """Test get_info for all bots using ASF."""
        controller = BotController(mock_ipc_handler)
        mock_response = {"Success": True, "Result": {}}

        with patch.object(mock_ipc_handler, "get", return_value=mock_response) as mock_get:
            result = await controller.get_info("ASF")
            assert result["Success"] is True
            mock_get.assert_called_once_with("/Bot/ASF", None)

    @pytest.mark.asyncio
    async def test_start(self, mock_ipc_handler):
        """Test start method."""
        controller = BotController(mock_ipc_handler)
        mock_response = {"Success": True, "Message": "Bot started"}

        with patch.object(mock_ipc_handler, "post", return_value=mock_response) as mock_post:
            result = await controller.start("test_bot")
            assert result["Success"] is True
            mock_post.assert_called_once_with("/Bot/test_bot/Start", None)

    @pytest.mark.asyncio
    async def test_stop(self, mock_ipc_handler):
        """Test stop method."""
        controller = BotController(mock_ipc_handler)
        mock_response = {"Success": True, "Message": "Bot stopped"}

        with patch.object(mock_ipc_handler, "post", return_value=mock_response) as mock_post:
            result = await controller.stop("test_bot")
            assert result["Success"] is True
            mock_post.assert_called_once_with("/Bot/test_bot/Stop", None)

    @pytest.mark.asyncio
    async def test_pause(self, mock_ipc_handler):
        """Test pause method."""
        controller = BotController(mock_ipc_handler)
        mock_response = {"Success": True, "Message": "Bot paused"}

        with patch.object(mock_ipc_handler, "post", return_value=mock_response) as mock_post:
            result = await controller.pause("test_bot")
            assert result["Success"] is True
            mock_post.assert_called_once_with("/Bot/test_bot/Pause", None)

    @pytest.mark.asyncio
    async def test_resume(self, mock_ipc_handler):
        """Test resume method."""
        controller = BotController(mock_ipc_handler)
        mock_response = {"Success": True, "Message": "Bot resumed"}

        with patch.object(mock_ipc_handler, "post", return_value=mock_response) as mock_post:
            result = await controller.resume("test_bot")
            assert result["Success"] is True
            mock_post.assert_called_once_with("/Bot/test_bot/Resume", None)

    @pytest.mark.asyncio
    async def test_redeem_single_key(self, mock_ipc_handler):
        """Test redeem with single key."""
        controller = BotController(mock_ipc_handler)
        mock_response = {"Success": True, "Result": {}}

        with patch.object(mock_ipc_handler, "post", return_value=mock_response) as mock_post:
            result = await controller.redeem("test_bot", "XXXXX-XXXXX-XXXXX")
            assert result["Success"] is True
            mock_post.assert_called_once()
            call_args = mock_post.call_args
            assert call_args[0][0] == "/Bot/test_bot/Redeem"
            assert call_args[0][1]["KeysToRedeem"] == ["XXXXX-XXXXX-XXXXX"]

    @pytest.mark.asyncio
    async def test_redeem_multiple_keys(self, mock_ipc_handler):
        """Test redeem with multiple keys."""
        controller = BotController(mock_ipc_handler)
        keys = ["KEY1", "KEY2", "KEY3"]
        mock_response = {"Success": True, "Result": {}}

        with patch.object(mock_ipc_handler, "post", return_value=mock_response) as mock_post:
            result = await controller.redeem("test_bot", keys)
            assert result["Success"] is True
            call_args = mock_post.call_args
            assert call_args[0][1]["KeysToRedeem"] == keys

    @pytest.mark.asyncio
    async def test_add_license(self, mock_ipc_handler):
        """Test add_license method."""
        controller = BotController(mock_ipc_handler)
        licenses = [12345, 67890]
        mock_response = {"Success": True, "Message": "Licenses added"}

        with patch.object(mock_ipc_handler, "post", return_value=mock_response) as mock_post:
            result = await controller.add_license("test_bot", licenses)
            assert result["Success"] is True
            call_args = mock_post.call_args
            assert call_args[0][1]["Licenses"] == licenses

    @pytest.mark.asyncio
    async def test_get_inventory_general(self, mock_ipc_handler):
        """Test get_inventory without specific app."""
        controller = BotController(mock_ipc_handler)
        mock_response = {"Success": True, "Result": {}}

        with patch.object(mock_ipc_handler, "get", return_value=mock_response) as mock_get:
            result = await controller.get_inventory("test_bot")
            assert result["Success"] is True
            mock_get.assert_called_once_with("/Bot/test_bot/Inventory", None)

    @pytest.mark.asyncio
    async def test_get_inventory_specific_app(self, mock_ipc_handler):
        """Test get_inventory with specific app and context."""
        controller = BotController(mock_ipc_handler)
        mock_response = {"Success": True, "Result": {}}

        with patch.object(mock_ipc_handler, "get", return_value=mock_response) as mock_get:
            result = await controller.get_inventory("test_bot", app_id=753, context_id=6)
            assert result["Success"] is True
            mock_get.assert_called_once_with("/Bot/test_bot/Inventory/753/6", None)

    @pytest.mark.asyncio
    async def test_input(self, mock_ipc_handler):
        """Test input method."""
        controller = BotController(mock_ipc_handler)
        mock_response = {"Success": True, "Message": "Input accepted"}

        with patch.object(mock_ipc_handler, "post", return_value=mock_response) as mock_post:
            result = await controller.input("test_bot", "SteamGuard", "ABCDE")
            assert result["Success"] is True
            call_args = mock_post.call_args
            assert call_args[0][1]["Type"] == "SteamGuard"
            assert call_args[0][1]["Value"] == "ABCDE"

    @pytest.mark.asyncio
    async def test_rename(self, mock_ipc_handler):
        """Test rename method."""
        controller = BotController(mock_ipc_handler)
        mock_response = {"Success": True, "Message": "Bot renamed"}

        with patch.object(mock_ipc_handler, "post", return_value=mock_response) as mock_post:
            result = await controller.rename("old_name", "new_name")
            assert result["Success"] is True
            call_args = mock_post.call_args
            assert call_args[0][0] == "/Bot/old_name/Rename"
            assert call_args[0][1]["NewName"] == "new_name"

    @pytest.mark.asyncio
    async def test_delete(self, mock_ipc_handler):
        """Test delete method."""
        controller = BotController(mock_ipc_handler)
        mock_response = {"Success": True, "Message": "Bot deleted"}

        with patch.object(mock_ipc_handler, "delete", return_value=mock_response) as mock_delete:
            result = await controller.delete("test_bot")
            assert result["Success"] is True
            mock_delete.assert_called_once_with("/Bot/test_bot", None)


class TestCommandController:
    """Test CommandController methods."""

    @pytest.mark.asyncio
    async def test_execute(self, mock_ipc_handler):
        """Test execute method."""
        controller = CommandController(mock_ipc_handler)
        mock_response = {"Success": True, "Result": "Command executed"}

        with patch.object(mock_ipc_handler, "post", return_value=mock_response) as mock_post:
            result = await controller.execute("status ASF")
            assert result["Success"] is True
            call_args = mock_post.call_args
            assert call_args[0][1]["Command"] == "status ASF"


class TestNLogController:
    """Test NLogController methods."""

    @pytest.mark.asyncio
    async def test_get_log_file(self, mock_ipc_handler):
        """Test get_log_file method."""
        controller = NLogController(mock_ipc_handler)
        mock_response = {"Success": True, "Result": "Log content here"}

        with patch.object(mock_ipc_handler, "get", return_value=mock_response) as mock_get:
            result = await controller.get_log_file()
            assert result["Success"] is True
            mock_get.assert_called_once_with("/NLog/File", None)


class TestTypeController:
    """Test TypeController methods."""

    @pytest.mark.asyncio
    async def test_get_type(self, mock_ipc_handler):
        """Test get_type method."""
        controller = TypeController(mock_ipc_handler)
        type_name = "ArchiSteamFarm.Steam.Storage.BotConfig"
        mock_response = {"Success": True, "Result": {"TypeName": type_name}}

        with patch.object(mock_ipc_handler, "get", return_value=mock_response) as mock_get:
            result = await controller.get_type(type_name)
            assert result["Success"] is True
            mock_get.assert_called_once_with(f"/Type/{type_name}", None)


class TestStructureController:
    """Test StructureController methods."""

    @pytest.mark.asyncio
    async def test_get_structure(self, mock_ipc_handler):
        """Test get_structure method."""
        controller = StructureController(mock_ipc_handler)
        structure_name = "ArchiSteamFarm.Storage.GlobalConfig"
        mock_response = {"Success": True, "Result": {"StructureName": structure_name}}

        with patch.object(mock_ipc_handler, "get", return_value=mock_response) as mock_get:
            result = await controller.get_structure(structure_name)
            assert result["Success"] is True
            mock_get.assert_called_once_with(f"/Structure/{structure_name}", None)
