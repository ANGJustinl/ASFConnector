from .BaseController import BaseController


class NLogController(BaseController):
    """Controller for NLog-related API endpoints"""

    async def get_log_file(self):
        """
        GET /Api/NLog/File
        Fetches ASF log file.

        Returns:
            dict: API response with log file content
        """
        return await self._get("/NLog/File")

    async def get_log_stream(self):
        """
        GET /Api/NLog
        Establishes WebSocket connection for real-time logs.

        Note: This endpoint requires WebSocket connection and is not currently supported
        by this library. Use a WebSocket client to connect to this endpoint directly.

        WebSocket URL: ws://your_host:your_port/Api/NLog

        Returns:
            dict: Information about WebSocket requirement
        """
        self.logger.warning("WebSocket endpoint - requires WebSocket client for real-time log streaming")
        return {
            "Success": False,
            "Message": "This endpoint requires WebSocket connection. Use WebSocket client to connect to ws://host:port/Api/NLog",
        }
