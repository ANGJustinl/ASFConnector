from .BaseController import BaseController

class TwoFactorAuthenticationController(BaseController):
    """Controller for TwoFactorAuthentication-related API endpoints"""
    
    async def get_token(self, bot_names: str):
        """
        GET /Api/Bot/{botNames}/TwoFactorAuthentication/Token
        Fetches 2FA tokens of given bots.
        
        Requires ASF 2FA module to be active on the specified bots.
        
        Args:
            bot_names: Bot name(s), can use ASF for all bots
            
        Returns:
            dict: API response with 2FA tokens
            
        Example:
            tokens = await connector.twofa.get_token('bot1')
            if tokens.get('Success'):
                for bot_name, token_data in tokens['Result'].items():
                    print(f"{bot_name}: {token_data['Result']}")
        """
        resource = f'/Bot/{bot_names}/TwoFactorAuthentication/Token'
        return await self._get(resource)