from .BaseController import BaseController

class TypeController(BaseController):
    """Controller for Type-related API endpoints"""
    
    async def get_type(self, type_name: str):
        """
        GET /Api/Type/{type}
        Fetches type information for a given type.
        
        Args:
            type_name: The type name to query
            
        Returns:
            dict: API response with type information
        """
        resource = f'/Type/{type_name}'
        return await self._get(resource)