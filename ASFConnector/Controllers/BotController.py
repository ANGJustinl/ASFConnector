from typing import Optional

from .BaseController import BaseController


class BotController(BaseController):
    """Controller for Bot-related API endpoints"""

    async def get_info(self, bot_names: str):
        """
        GET /Api/Bot/{botNames}
        Fetches information about specified bots.

        Args:
            bot_names: Bot name(s), can use ASF for all bots

        Returns:
            dict: Bot information
        """
        resource = f"/Bot/{bot_names}"
        return await self._get(resource)

    async def update_config(self, bot_names: str, config: dict):
        """
        POST /Api/Bot/{botNames}
        Updates configuration of specified bots.

        Args:
            bot_names: Bot name(s), can use ASF for all bots
            config: Bot configuration dict to update

        Returns:
            dict: API response
        """
        resource = f"/Bot/{bot_names}"
        return await self._post(resource, payload=config)

    async def delete(self, bot_names: str):
        """
        DELETE /Api/Bot/{botNames}
        Deletes all files related to specified bots.

        Args:
            bot_names: Bot name(s), can use ASF for all bots

        Returns:
            dict: API response
        """
        resource = f"/Bot/{bot_names}"
        return await self._delete(resource)

    async def start(self, bot_names: str):
        """
        POST /Api/Bot/{botNames}/Start
        Starts specified bots.

        Args:
            bot_names: Bot name(s), can use ASF for all bots

        Returns:
            dict: API response
        """
        resource = f"/Bot/{bot_names}/Start"
        return await self._post(resource)

    async def stop(self, bot_names: str):
        """
        POST /Api/Bot/{botNames}/Stop
        Stops specified bots.

        Args:
            bot_names: Bot name(s), can use ASF for all bots

        Returns:
            dict: API response
        """
        resource = f"/Bot/{bot_names}/Stop"
        return await self._post(resource)

    async def pause(self, bot_names: str):
        """
        POST /Api/Bot/{botNames}/Pause
        Pauses specified bots.

        Args:
            bot_names: Bot name(s), can use ASF for all bots

        Returns:
            dict: API response
        """
        resource = f"/Bot/{bot_names}/Pause"
        return await self._post(resource)

    async def resume(self, bot_names: str):
        """
        POST /Api/Bot/{botNames}/Resume
        Resumes specified bots.

        Args:
            bot_names: Bot name(s), can use ASF for all bots

        Returns:
            dict: API response
        """
        resource = f"/Bot/{bot_names}/Resume"
        return await self._post(resource)

    async def redeem(self, bot_names: str | list | set, keys):
        """
        POST /Api/Bot/{botNames}/Redeem
        Redeems cd-keys on specified bots.

        Args:
            bot_names: Bot name(s), can use ASF for all bots
            keys: Single key string or set/list of keys

        Returns:
            dict: API response with redemption results
        """
        self.logger.debug(f"bot_redeem: bot {bot_names}, keys {keys}")

        # Convert keys to list format
        if isinstance(keys, str):
            payload_keys = [keys]
        else:
            payload_keys = list(keys)

        resource = f"/Bot/{bot_names}/Redeem"
        data = {"KeysToRedeem": payload_keys}
        return await self._post(resource, payload=data)

    async def add_license(self, bot_names: str, licenses):
        """
        POST /Api/Bot/{botNames}/AddLicense
        Adds free licenses on specified bots.

        Args:
            bot_names: Bot name(s), can use ASF for all bots
            licenses: License IDs to add

        Returns:
            dict: API response
        """
        resource = f"/Bot/{bot_names}/AddLicense"
        if isinstance(licenses, (list, set)):
            payload = {"Licenses": list(licenses)}
        else:
            payload = {"Licenses": [licenses]}
        return await self._post(resource, payload=payload)

    async def get_inventory(
        self,
        bot_names: str,
        app_id: Optional[int] = None,
        context_id: Optional[int] = None,
    ):
        """
        GET /Api/Bot/{botNames}/Inventory or /Api/Bot/{botNames}/Inventory/{appID}/{contextID}
        Fetches inventory information of specified bots.

        Args:
            bot_names: Bot name(s), can use ASF for all bots
            app_id: Optional app ID for specific inventory
            context_id: Optional context ID for specific inventory

        Returns:
            dict: Inventory information
        """
        if app_id and context_id:
            resource = f"/Bot/{bot_names}/Inventory/{app_id}/{context_id}"
        else:
            resource = f"/Bot/{bot_names}/Inventory"
        return await self._get(resource)

    async def input(self, bot_names: str, input_type: str, input_value: str):
        """
        POST /Api/Bot/{botNames}/Input
        Provides input value to bot for next usage.

        Args:
            bot_names: Bot name(s)
            input_type: Type of input (e.g., "DeviceID", "SteamGuard")
            input_value: Input value to provide

        Returns:
            dict: API response
        """
        resource = f"/Bot/{bot_names}/Input"
        payload = {"Type": input_type, "Value": input_value}
        return await self._post(resource, payload=payload)

    async def rename(self, bot_name: str, new_name: str):
        """
        POST /Api/Bot/{botName}/Rename
        Renames bot along with all related files.

        Args:
            bot_name: Current bot name (single bot only)
            new_name: New bot name

        Returns:
            dict: API response
        """
        resource = f"/Bot/{bot_name}/Rename"
        payload = {"NewName": new_name}
        return await self._post(resource, payload=payload)

    async def get_games_to_redeem_in_background(self, bot_names: str):
        """
        GET /Api/Bot/{botNames}/GamesToRedeemInBackground
        Fetches background game redeemer output.

        Args:
            bot_names: Bot name(s), can use ASF for all bots

        Returns:
            dict: Background game redeemer information
        """
        resource = f"/Bot/{bot_names}/GamesToRedeemInBackground"
        return await self._get(resource)

    async def add_games_to_redeem_in_background(
        self, bot_names: str, games_to_redeem: dict
    ):
        """
        POST /Api/Bot/{botNames}/GamesToRedeemInBackground
        Adds keys to background game redeemer.

        Args:
            bot_names: Bot name(s), can use ASF for all bots
            games_to_redeem: Dict of games to redeem

        Returns:
            dict: API response
        """
        resource = f"/Bot/{bot_names}/GamesToRedeemInBackground"
        return await self._post(resource, payload=games_to_redeem)

    async def delete_games_to_redeem_in_background(self, bot_names: str):
        """
        DELETE /Api/Bot/{botNames}/GamesToRedeemInBackground
        Removes background game redeemer output files.

        Args:
            bot_names: Bot name(s), can use ASF for all bots

        Returns:
            dict: API response
        """
        resource = f"/Bot/{bot_names}/GamesToRedeemInBackground"
        return await self._delete(resource)

    async def redeem_points(self, bot_names: str, definition_id: int):
        """
        POST /Api/Bot/{botNames}/RedeemPoints/{definitionID}
        Redeems points on specified bots.

        Args:
            bot_names: Bot name(s), can use ASF for all bots
            definition_id: Definition ID of item to redeem

        Returns:
            dict: API response
        """
        resource = f"/Bot/{bot_names}/RedeemPoints/{definition_id}"
        return await self._post(resource)
