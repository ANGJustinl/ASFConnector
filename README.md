<div align="center">

# ASFConnector API

ASFConnector is an asynchronous Python client for interacting with the ArchiSteamFarm (ASF) IPC API. It features a modular architecture with connection pool reuse, providing high-performance API call experience.

<img src="https://img.shields.io/github/license/ANGJustinl/ASFConnector" alt="license">
<img src="https://img.shields.io/badge/python-3.10+-blue.svg" alt="python">
<img src="https://img.shields.io/badge/asyncio-supported-brightgreen.svg" alt="asyncio">
<img src="https://img.shields.io/badge/ASF-6.2.2.3--latest%20supported-black.svg" alt="ASF">
<img src="https://img.shields.io/badge/code%20style-ruff-black?logo=ruff" alt="ruff">
<img src="https://results.pre-commit.ci/badge/github/ANGJustinl/nonebot_plugin_archisteamfarm/master.svg" alt="pre-commit">
</div>

### [Chinese | 中文文档](./docs/README_zh.md)
### [API Implementation Details](./API.md)

## Architecture Design

### Core Components

1. **ASFConnector** (`__init__.py`)
   - Main entry class managing connection lifecycle
   - Unified management of all Controller instances
   - Supports `async with` context manager for connection pool reuse

2. **IPCProtocolHandler** (`IPCProtocol.py`)
   - Low-level HTTP client wrapper
   - Implements asynchronous requests using `httpx.AsyncClient`
   - Supports connection pool reuse for improved performance

3. **BaseController** (`BaseController.py`)
   - Base class for all Controllers
   - Provides common GET/POST/DELETE request methods
   - Unified logging

4. **ASFConfig** (`config.py`)
   - Pydantic-based configuration management
   - Supports loading configuration from .env files
   - Automatic parameter validation

5. **Controller Modules**
   - **ASFController**: ASF global operations (get info, update config, restart, etc.)
   - **BotController**: Bot-related operations (start, stop, redeem, etc.)
   - **NLogController**: Logging operations (retrieve log files)
   - **TypeController**: Type information queries
   - **StructureController**: Structure information queries
   - **CommandController**: Command execution (marked as legacy)

## Quick Start

> **⚠️ IMPORTANT: Configure Default Bot in ASF**
>
> Before using any Bot-related operations with this library, you **MUST** configure a `DefaultBot` in your ASF global configuration. Without this setting, all Bot-related operations may exhibit random behavior and produce unexpected results.
>
> Add the following to your ASF `ASF.json` configuration file:
> ```json
> {
>   "DefaultBot": "your_primary_bot_name"
> }
> ```
>
> For more details, see: [ASF Configuration - DefaultBot](https://github.com/JustArchiNET/ArchiSteamFarm/wiki/Configuration#defaultbot)

### Configuration Setup

1. Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```

2. Edit the `.env` file:
```env
ASF_HOST=127.0.0.1
ASF_PORT=1242
ASF_PASSWORD=your_ipc_password
ENABLE_RICH_TRACEBACK=False
```

### Basic Usage (Recommended)

Use `.env` configuration file with automatic loading:

```python
import asyncio
from ASFConnector import ASFConnector

async def main():
    # Auto-load configuration from .env file
    async with ASFConnector.from_config() as connector:
        # Get ASF info
        asf_info = await connector.asf.get_info()
        print(f"ASF Version: {asf_info['Result']['Version']}")
        
        # Get Bot info
        bot_info = await connector.bot.get_info('bot_name')
        print(bot_info)

asyncio.run(main())
```

### Using Custom Configuration

```python
import asyncio
from ASFConnector import ASFConnector
from ASFConnector.config import ASFConfig

async def main():
    # Create custom configuration
    config = ASFConfig(
        asf_host='192.168.1.100',
        asf_port='8080',
        asf_password='my_password'
    )
    
    async with ASFConnector.from_config(config) as connector:
        info = await connector.asf.get_info()
        print(info)

asyncio.run(main())
```

### Direct Parameters (Backward Compatible)

```python
import asyncio
from ASFConnector import ASFConnector

async def main():
    # Create connection with direct parameters
    async with ASFConnector(
        host='127.0.0.1',
        port='1242',
        password='your_ipc_password'
    ) as connector:
        info = await connector.asf.get_info()
        print(f"Request: {info['Success']}")

asyncio.run(main())
```

## API Reference

### ASFController

#### `get_info()`
Get ASF global information.

```python
info = await connector.asf.get_info()
```

**Response Example:**
```json
{
    "Success": true,
    "Result": {
        "Version": "5.4.0.3",
        "BuildVariant": "generic",
        ...
    }
}
```

#### `update_config(config: dict)`
Update ASF global configuration.

```python
config = {
    "AutoRestart": True,
    "UpdatePeriod": 24
}
result = await connector.asf.update_config(config)
```

#### `exit()`
Shut down ASF.

```python
result = await connector.asf.exit()
```

#### `restart()`
Restart ASF.

```python
result = await connector.asf.restart()
```

#### `update()`
Update ASF to the latest stable version.

```python
result = await connector.asf.update()
```

#### `encrypt(data: dict)`
Encrypt data using ASF encryption mechanisms.

```python
data = {
    "CryptoMethod": 0,  # Encryption method (0 = AES)
    "StringToEncrypt": "my_sensitive_data"
}
result = await connector.asf.encrypt(data)
```

#### `hash(data: dict)`
Hash data using ASF hashing mechanisms.

```python
data = {
    "HashMethod": 0,  # Hashing method (0 = SHA256)
    "StringToHash": "my_string_to_hash"
}
result = await connector.asf.hash(data)
```

### BotController

#### `get_info(bot_names: str)`
Get information for specified Bot(s).

```python
# Single Bot
info = await connector.bot.get_info('bot1')

# Multiple Bots (comma-separated)
info = await connector.bot.get_info('bot1,bot2')

# All Bots
info = await connector.bot.get_info('ASF')
```

#### `start(bot_names: str)`
Start specified Bot(s).

```python
result = await connector.bot.start('bot1')
```

#### `stop(bot_names: str)`
Stop specified Bot(s).

```python
result = await connector.bot.stop('bot1')
```

#### `pause(bot_names: str)`
Pause card farming for specified Bot(s).

```python
result = await connector.bot.pause('bot1')
```

#### `resume(bot_names: str)`
Resume card farming for specified Bot(s).

```python
result = await connector.bot.resume('bot1')
```

#### `redeem(bot_names: str, keys)`
Redeem CD-Keys on specified Bot(s).

```python
# Single key
result = await connector.bot.redeem('bot1', 'XXXXX-XXXXX-XXXXX')

# Multiple keys
keys = ['KEY1', 'KEY2', 'KEY3']
result = await connector.bot.redeem('bot1', keys)
```

#### `add_license(bot_names: str, licenses)`
Add free licenses.

```python
result = await connector.bot.add_license('bot1', [12345, 67890])
```

#### `get_inventory(bot_names: str, app_id: int = None, context_id: int = None)`
Get inventory information.

```python
# Get general inventory
inventory = await connector.bot.get_inventory('bot1')

# Get specific game inventory (Steam trading cards)
inventory = await connector.bot.get_inventory('bot1', app_id=753, context_id=6)
```

#### `input(bot_names: str, input_type: str, input_value: str)`
Provide input value for Bot (e.g., Steam Guard code).

```python
result = await connector.bot.input('bot1', 'SteamGuard', 'ABCDE')
```

#### `rename(bot_name: str, new_name: str)`
Rename a Bot.

```python
result = await connector.bot.rename('old_bot_name', 'new_bot_name')
```

#### `delete_games_to_redeem_in_background(bot_names: str)`
Delete background game redemption output files.

```python
result = await connector.bot.delete_games_to_redeem_in_background('bot1')
```

### NLogController

#### `get_log_file()`
Get ASF log file content.

```python
log_content = await connector.nlog.get_log_file()
if log_content.get('Success'):
    print(log_content['Result'])
```

#### `get_log_stream()`
Get real-time log stream (requires WebSocket support).

```python
# Note: This endpoint requires a WebSocket client
# Currently returns instructions on how to use WebSocket connection
result = await connector.nlog.get_log_stream()
```

### TypeController

#### `get_type(type_name: str)`
Get type information for the specified type.

```python
type_info = await connector.type.get_type('ArchiSteamFarm.Steam.Storage.BotConfig')
```

### StructureController

#### `get_structure(structure_name: str)`
Get default structure for the specified type.

```python
structure = await connector.structure.get_structure('ArchiSteamFarm.Storage.GlobalConfig')
```

### CommandController (IPC API Legacy Feature)

> **Note:** This Controller has been marked as legacy by ASF. It's recommended to use specific methods from ASFController and BotController.

#### `execute(command: str)`
Execute a command.

```python
result = await connector.command.execute('status ASF')
```

## Configuration Management

### Configuration Validation

ASFConfig uses Pydantic for configuration validation:

```python
from ASFConnector.config import ASFConfig
from pydantic import ValidationError

try:
    config = ASFConfig(
        asf_host='127.0.0.1',
        asf_port='1242',  # Automatic port range validation (1-65535)
        asf_path='Api'    # Automatically adds leading slash -> '/Api'
    )
    config.log_config()
except ValidationError as e:
    print(f"Configuration validation failed: {e}")
```

### Configuration Parameters

| Parameter | Environment Variable | Default | Description |
|-----------|---------------------|---------|-------------|
| `asf_host` | `ASF_HOST` | `127.0.0.1` | ASF IPC host address |
| `asf_port` | `ASF_PORT` | `1242` | ASF IPC port (1-65535) |
| `asf_password` | `ASF_PASSWORD` | `None` | ASF IPC password (optional) |
| `asf_path` | `ASF_PATH` | `/Api` | ASF IPC API path |

## Performance Optimization

### Connection Pool Reuse

Using the `async with` context manager significantly improves performance:

```python
# Without connection pool (creates new connection for each request)
async with ASFConnector.from_config() as connector:
    await connector.asf.get_info()  # Slower

# With connection pool (reuses connections, recommended)
async with ASFConnector.from_config() as connector:
    for i in range(100):
        await connector.asf.get_info()  # Much faster!
```

### Performance Comparison

Based on test results (10 requests):
```
Results for 10 requests:
  Legacy API (no pool):     0.109s (10.9ms per request)
  New Controller (no pool): 0.111s (11.1ms per request)
  New Controller (w/ pool): 0.004s (0.4ms per request)

Speedup with connection pool: 28.51x faster
Time saved per request: 10.7ms
```


## Error Handling

All API calls return a dictionary containing a `Success` field:

```python
response = await connector.asf.get_info()

if response.get('Success'):
    data = response.get('Result')
    print(f"Success: {data}")
else:
    error_msg = response.get('Message', 'Unknown error')
    print(f"Error: {error_msg}")
```

When IPC requests trigger HTTP/network exceptions, the response dictionary will also include:

- `ExceptionType`: The corresponding custom exception class name (e.g., `ASF_NotFound`)
- `Exception`: The specific exception instance with `status_code` and original `payload`
- `StatusCode`: HTTP status code (if available)
- `ResponsePayload`: JSON or plain text content returned by ASF (if available)

The library provides unified exception definitions, accessible through the top-level `ASFConnector` export or the `ASFConnector.error` module:

```python
from ASFConnector import ASF_BadRequest, ASF_NotFound

response = await connector.type.get_type('ArchiSteamFarm.Storage.UnknownType')
if not response['Success']:
    exc = response['Exception']
    if isinstance(exc, ASF_NotFound):
        print("Type does not exist, original response:", response.get('ResponsePayload'))
    else:
        raise exc  # Raise or log as needed
```

All built-in exceptions inherit from `ASFConnectorError`. Common HTTP status code to exception mappings:

| HTTP Status Code | Exception Type |
|------------------|----------------|
| 400 | `ASF_BadRequest` |
| 401 | `ASF_Unauthorized` |
| 403 | `ASF_Forbidden` |
| 404 | `ASF_NotFound` |
| 405 | `ASF_NotAllowed` |
| 406 | `ASF_NotAcceptable` |
| 411 | `ASF_LengthRequired` |
| 501 | `ASF_NotImplemented` |


## More Information

- [API Implementation Details](./docs/API.md)
- [ASF IPC API Documentation](https://github.com/JustArchiNET/ArchiSteamFarm/wiki/IPC)
- [ASF Wiki](https://github.com/JustArchiNET/ArchiSteamFarm/wiki)

## Special Thanks:
- [ArchiSteamFarm](https://github.com/JustArchiNET/ArchiSteamFarm) for developing and maintaining ArchiSteamFarm.
- [dmcallejo/ASFBot](https://github.com/dmcallejo/ASFBot). for inspiring the architecture design of this library.
