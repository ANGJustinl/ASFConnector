# 25.10.28 Modified by angjustinl from dmcallejo/ASFBot/IPCProtocol
# source code at https://github.com/dmcallejo/ASFBot
# More informations see https://deepwiki.com/JustArchiNET/ArchiSteamFarm/4.1-api-controllers#asfcontroller
import httpx
import sys
from pathlib import Path
from typing import Optional
from loguru import logger

# Configure loguru logger
# Remove default handler
logger.remove()

# Add console handler with INFO level
logger.add(
    sys.stderr,
    level="INFO",
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
)

# Add file handler with DEBUG level
log_dir = Path("logs")
log_dir.mkdir(exist_ok=True)
logger.add(
    log_dir / "debug.log",
    level="DEBUG",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
    rotation="10 MB",  # Rotate when file reaches 10 MB
    retention="7 days",  # Keep logs for 7 days
    compression="zip"  # Compress rotated logs
)

logger.info("ASFConnector logger initialized")

from .IPCProtocol import IPCProtocolHandler
from .Controllers.enum import PurchaseResultDetail, Result
from .Controllers.ASFController import ASFController
from .Controllers.BotController import BotController
from .Controllers.CommandController import CommandController
from . import error as error_module
from .Controllers.NLogController import NLogController
from .Controllers.TypeController import TypeController
from .Controllers.StructureController import StructureController
from .Controllers.TwoFactorAuthenticationController import TwoFactorAuthenticationController
from .config import ASFConfig, load_config
from .error import (
    ASFConnectorError,
    ASFIPCError,
    ASFHTTPError,
    ASFNetworkError,
    ASF_BadRequest,
    ASF_Unauthorized,
    ASF_Forbidden,
    ASF_NotFound,
    ASF_NotAllowed,
    ASF_NotAcceptable,
    ASF_LengthRequired,
    ASF_NotImplemented,
    HTTP_STATUS_EXCEPTION_MAP,
)
class ASFConnector:
    """
    Main connector class for ASF API with connection pool management.
    
    Usage:
        # Method 1: Using config from .env file (recommended)
        async with ASFConnector.from_config() as connector:
            info = await connector.asf.get_info()
        
        # Method 2: With explicit parameters and context manager (connection pool reuse)
        async with ASFConnector(host='127.0.0.1', port='1242', password='your_password') as connector:
            info = await connector.asf.get_info()
            
        # Method 3: Without context manager (creates temporary connections)
        connector = ASFConnector(host='127.0.0.1', port='1242', password='your_password')
        info = await connector.asf.get_info()
    """

    def __init__(self, host: Optional[str] = None, port: Optional[str] = None, path: Optional[str] = None, password: Optional[str] = None, config: Optional[ASFConfig] = None):
        global logger
        logger = logger

        # If config object is provided, use it; otherwise use provided parameters or defaults
        if config:
            self.host = config.asf_host
            self.port = config.asf_port
            self.path = config.asf_path
            password = config.asf_password
            logger.debug("ASFConnector initialized from config object")
        else:
            self.host = host or '127.0.0.1'
            self.port = port or '1242'
            self.path = path or '/Api'
            logger.debug(f"ASFConnector initialized with parameters")

        logger.info(f"{__name__} initialized. Host: '{self.host}'. Port: '{self.port}'")
        # Create shared connection handler for all controllers
        self.connection_handler = IPCProtocolHandler(self.host, self.port, self.path, password)
        self.error = error_module
        
        # Initialize controllers with shared connection handler
        self.asf = ASFController(self.connection_handler)
        self.bot = BotController(self.connection_handler)
        self.command = CommandController(self.connection_handler)
        self.nlog = NLogController(self.connection_handler)
        self.type = TypeController(self.connection_handler)
        self.structure = StructureController(self.connection_handler)
        self.twofa = TwoFactorAuthenticationController(self.connection_handler)
    
    @classmethod
    def from_config(cls, config: Optional[ASFConfig] = None):
        """
        Create ASFConnector from configuration.
        
        Args:
            config: ASFConfig object. If None, loads from .env file
            
        Returns:
            ASFConnector: New connector instance
            
        Example:
            # Load from .env
            connector = ASFConnector.from_config()
            
            # Or with custom config
            config = ASFConfig(asf_host='192.168.1.100', asf_port='8080')
            connector = ASFConnector.from_config(config)
        """
        if config is None:
            config = load_config()
        return cls(config=config)
    
    async def __aenter__(self):
        """Enable connection pool reuse via context manager"""
        await self.connection_handler.__aenter__()
        logger.debug("ASFConnector connection pool activated")
        
        # Perform health check
        health = await self.health_check()
        if not health.get('Success'):
            logger.warning(f"Health check failed: {health.get('Message', 'Unknown error')}")
        else:
            logger.info("ASF health check passed")
        
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Clean up connection pool"""
        await self.connection_handler.__aexit__(exc_type, exc_val, exc_tb)
        logger.debug("ASFConnector connection pool closed")
    
    async def health_check(self):
        """
        GET /HealthCheck
        Checks ASF health status.
        
        Note: This endpoint is at the root level, not under /Api
        
        Returns:
            dict: Health check response with status code
            Returns {"Success": True, "Message": "OK"} if status is 200
        """
        # Build direct URL to /HealthCheck (not /Api/HealthCheck)
        health_url = f'http://{self.host}:{self.port}/HealthCheck'
        
        # Use connection handler's client if available
        if self.connection_handler._client:
            client = self.connection_handler._client
            should_close = False
        else:
            client = httpx.AsyncClient(headers=self.connection_handler.headers)
            should_close = True
        
        try:
            response = await client.get(health_url)
            response.raise_for_status()
            logger.debug(f"Health check: {response.url} - {response.status_code}")
            
            # Try to parse JSON response
            try:
                data = response.json()
                # If it's already a proper response, return it
                if 'Success' in data:
                    return data
                # Otherwise wrap it
                return {
                    'Success': True,
                    'Message': data.get('Message', 'OK'),
                    'Result': data
                }
            except Exception:
                # If not JSON or parsing fails, just check status code
                if response.status_code == 200:
                    return {
                        'Success': True,
                        'Message': response.text or 'OK',
                        'StatusCode': response.status_code
                    }
                else:
                    return {
                        'Success': False,
                        'Message': f'HTTP {response.status_code}',
                        'StatusCode': response.status_code
                    }
        except Exception as ex:
            logger.error(f"Health check failed: {ex}")
            return {
                'Success': False,
                'Message': str(ex)
            }
        finally:
            if should_close:
                await client.aclose()

    async def get_asf_info(self):
        """
        Fetches common info related to ASF as a whole.
        
        Note: This method is kept for backward compatibility.
        New code should use: connector.asf.get_info()
        """
        return await self.asf.get_info()

    async def get_bot_info(self, bot):
        """
        Fetches common info related to given bots.
        
        Note: This method is kept for backward compatibility.
        New code should use: connector.bot.get_info(bot)
        """
        logger.debug(f'get_bot_info: bot {bot}')
        response = await self.bot.get_info(bot)
        if 'Result' in response:
            message = ""
            for bot_name in response['Result']:
                message += 'Bot {}: '.format(bot_name)
                bot = response['Result'][bot_name]
                if bot['IsConnectedAndLoggedOn']:
                    cards_farmer = bot['CardsFarmer']
                    farm_message = ""
                    if cards_farmer['Paused']:
                        farm_message += 'Farming paused.'
                    elif cards_farmer['CurrentGamesFarming']:
                        farm_message += 'Currently farming games:'
                    for current_games in cards_farmer['CurrentGamesFarming']:
                        appid = current_games['AppID']
                        appname = current_games['GameName']
                        cards_remaining = current_games['CardsRemaining']
                        farm_message += '\n\t[{}/{}] {} cards remaining.'.format(appid, appname, cards_remaining)
                    if len(cards_farmer['GamesToFarm']) > 0:
                        farm_message += ' {} game(s) to farm ('.format(len(cards_farmer['GamesToFarm']))
                        for games_to_farm in cards_farmer['GamesToFarm']:
                            appid = games_to_farm['AppID']
                            appname = games_to_farm['GameName']
                            farm_message += '[{}/{}] '.format(appid, appname)
                        farm_message = farm_message[:-1] + "). "
                    time_remaining = cards_farmer['TimeRemaining']
                    if time_remaining != '00:00:00':
                        farm_message += 'Time remaining: {}'.format(time_remaining)
                    if len(farm_message) == 0:
                        farm_message += 'Idle.'
                    message += farm_message + '\n'
                else:
                    if len(bot['BotConfig']) == 0:
                        message += 'Not configured.\n'
                    else:
                        message += 'Offline.\n'
        elif response['Success']:
            message = 'Bot {} not found.'.format(bot)
        else:
            message = 'Getting bot info failed: {}'.format(response['Message'])
        return message

    async def bot_redeem(self, bot, keys):
        """
        Redeems cd-keys on given bot.
        
        Note: This method is kept for backward compatibility.
        New code should use: connector.bot.redeem(bot, keys)
        """
        response = await self.bot.redeem(bot, keys)
        if 'Result' in response:
            results = response['Result']
            message = ""
            for bot_name in results:
                bot = results[bot_name]
                for key in bot:
                    if bot[key]:
                        message += "Bot {}: \n".format(bot_name)
                        if 'purchase_receipt_info' in bot[key] and bot[key]['purchase_receipt_info']:
                            purchase_receipt_info = bot[key]['purchase_receipt_info']
                            items = ''
                            # Parse items in the key
                            for item in purchase_receipt_info['line_items']:
                                items += '[{}, {}] '.format(item['packageid'], item['line_item_description'])
                            # Build message with the receipt info and the items
                            message += "\t[{}] {}: {}/{}\n".format(
                                key, items, purchase_receipt_info['purchase_status']
                                if type(purchase_receipt_info['purchase_status']) is str
                                else Result[purchase_receipt_info['purchase_status']],
                                purchase_receipt_info['result_detail'] if type(purchase_receipt_info['result_detail']) is str
                                else PurchaseResultDetail[purchase_receipt_info['result_detail']])
                        else:
                            message += "\t[{}] {}/{}\n".format(
                                key, bot[key]['Result'] if type(bot[key]['Result']) is str
                                else Result[bot[key]['Result']],
                                bot[key]['PurchaseResultDetail'] if type(bot[key]['PurchaseResultDetail']) is str
                                else PurchaseResultDetail[bot[key]['PurchaseResultDetail']])

        elif response['Success']:
            message = 'Bot {} not found.'.format(bot)
        else:
            message = 'Redeem failed: {}'.format(response['Message'])
        return message

    async def send_command(self, command):
        """
        Executes a command (LEGACY method).
        
        Note: This method is kept for backward compatibility.
        New code should use: connector.command.execute(command)
        
        This API endpoint is supposed to be entirely replaced by ASF actions 
        available under /Api/ASF/{action} and /Api/Bot/{bot}/{action}.
        """
        response = await self.command.execute(command)
        message = ""
        if response.get('Success'):
            message += response.get('Result', '')
        else:
            message += 'Command unsuccessful: {}'.format(response.get('Message', 'Unknown error'))
        return message


__all__ = [
    "ASFConnector",
    "ASFConfig",
    "load_config",
    "ASFController",
    "BotController",
    "CommandController",
    "NLogController",
    "TypeController",
    "StructureController",
    "TwoFactorAuthenticationController",
    "PurchaseResultDetail",
    "Result",
    "error",
    "ASFConnectorError",
    "ASFIPCError",
    "ASFHTTPError",
    "ASFNetworkError",
    "ASF_BadRequest",
    "ASF_Unauthorized",
    "ASF_Forbidden",
    "ASF_NotFound",
    "ASF_NotAllowed",
    "ASF_NotAcceptable",
    "ASF_LengthRequired",
    "ASF_NotImplemented",
    "HTTP_STATUS_EXCEPTION_MAP",
]
