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
        return await self._get('/ASF')
    
    async def update_config(self, config: dict):
        """
        POST /Api/ASF
        Updates ASF's global configuration.
        
        Args:
            config: Global configuration dict to update
            
        Returns:
            dict: API response
        """
        return await self._post('/ASF', payload=config)
    
    async def exit(self):
        """
        POST /Api/ASF/Exit
        Shuts down ASF.
        
        Returns:
            dict: API response
        """
        return await self._post('/ASF/Exit')
    
    async def restart(self):
        """
        POST /Api/ASF/Restart
        Restarts ASF.
        
        Returns:
            dict: API response
        """
        return await self._post('/ASF/Restart')