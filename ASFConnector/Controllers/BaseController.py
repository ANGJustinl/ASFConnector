from loguru import logger

class BaseController:
    """Base controller class with shared connection handler and common utilities"""
    
    def __init__(self, connection_handler):
        """
        Initialize with shared connection handler from ASFConnector
        
        Args:
            connection_handler: IPCProtocolHandler instance managed by ASFConnector
        """
        self.logger = logger
        self.connection_handler = connection_handler
        self.logger.debug(f"{self.__class__.__name__} initialized")
    
    async def _get(self, resource, parameters=None):
        """
        Wrapper for GET requests with logging
        
        Args:
            resource: API resource path
            parameters: Optional query parameters
            
        Returns:
            API response dict
        """
        self.logger.debug(f"GET {resource} with params: {parameters}")
        return await self.connection_handler.get(resource, parameters)
    
    async def _post(self, resource, payload=None):
        """
        Wrapper for POST requests with logging and health check
        
        Args:
            resource: API resource path
            payload: Optional request body
            
        Returns:
            API response dict
        """
        self.logger.debug(f"POST {resource} with payload: {payload}")
        return await self.connection_handler.post(resource, payload)
    
    async def _delete(self, resource, parameters=None):
        """
        Wrapper for DELETE requests with logging

        Args:
            resource: API resource path
            parameters: Optional query parameters

        Returns:
            API response dict
        """
        self.logger.debug(f"DELETE {resource} with params: {parameters}")
        return await self.connection_handler.delete(resource, parameters)