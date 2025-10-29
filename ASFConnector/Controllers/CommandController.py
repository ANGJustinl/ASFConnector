from .BaseController import BaseController


class CommandController(BaseController):
    """
    Controller for Command-related API endpoints (LEGACY)

    Note: This API endpoint is marked as legacy by ASF.
    It is supposed to be entirely replaced by ASF actions available under:
    - /Api/ASF/{action}
    - /Api/Bot/{bot}/{action}

    Use specific controller methods (ASFController, BotController) instead when possible.
    """

    async def execute(self, command: str):
        """
        POST /Api/Command
        Executes a command.

        DEPRECATED: This endpoint is legacy. Use specific ASF or Bot actions instead.

        When executing this endpoint, you should use "given bot" commands.
        Omitting targets of the command will cause the command to be executed
        on the first defined bot.

        Args:
            command: Command string to execute

        Returns:
            dict: Command execution result
        """
        self.logger.debug(f"Execute command: {command}")
        self.logger.warning(
            "CommandController.execute() is a legacy endpoint. Consider using ASFController or BotController methods instead."
        )
        resource = "/Command"
        payload = {"Command": command}
        return await self._post(resource, payload=payload)
