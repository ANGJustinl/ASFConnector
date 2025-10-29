from .BaseController import BaseController


class StructureController(BaseController):
    """Controller for Structure-related API endpoints"""

    async def get_structure(self, structure_name: str):
        """
        GET /Api/Structure/{structure}
        Fetches default structure of a given type.

        Args:
            structure_name: The structure name to query

        Returns:
            dict: API response with structure information
        """
        resource = f"/Structure/{structure_name}"
        return await self._get(resource)
