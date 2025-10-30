from .BaseController import BaseController


class ASFController(BaseController):
    """Controller for ASF-related API endpoints"""

    async def get_info(self):
        """
        GET /Api/ASF
        Fetches common info related to ASF as a whole.

        Returns:
            dict: ASF information
        """
        return await self._get("/ASF")

    async def update_config(self, config: dict):
        """
        POST /Api/ASF
        Updates ASF's global configuration.

        Args:
            config: Global configuration dict to update

        Returns:
            dict: API response
        """
        return await self._post("/ASF", payload=config)

    async def exit(self):
        """
        POST /Api/ASF/Exit
        Shuts down ASF.

        Returns:
            dict: API response
        """
        return await self._post("/ASF/Exit")

    async def restart(self):
        """
        POST /Api/ASF/Restart
        Restarts ASF.

        Returns:
            dict: API response
        """
        return await self._post("/ASF/Restart")

    async def update(self):
        """
        POST /Api/ASF/Update
        Updates ASF to the latest stable version.

        Returns:
            dict: API response with update status
        """
        return await self._post("/ASF/Update")

    async def encrypt(self, data: dict):
        """
        POST /Api/ASF/Encrypt
        Encrypts data with ASF encryption mechanisms.

        Args:
            data: Dictionary containing data to encrypt. Should have structure:
                  {
                      "CryptoMethod": int (encryption method),
                      "StringToEncrypt": str (string to be encrypted)
                  }

        Returns:
            dict: API response with encrypted data
        """
        return await self._post("/ASF/Encrypt", payload=data)

    async def hash(self, data: dict):
        """
        POST /Api/ASF/Hash
        Hashes data with ASF hashing mechanisms.

        Args:
            data: Dictionary containing data to hash. Should have structure:
                  {
                      "HashMethod": int (hashing method),
                      "StringToHash": str (string to be hashed)
                  }

        Returns:
            dict: API response with hashed data
        """
        return await self._post("/ASF/Hash", payload=data)
