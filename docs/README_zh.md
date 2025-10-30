<div align="center">
<img src="../docs/img/logo.png" width="180" height="180" alt="ASFConnector">

# ASFConnector API

ASFConnector 是一个用于与 ArchiSteamFarm (ASF) IPC API 交互的异步 Python 客户端。采用模块化架构，支持连接池复用，提供高性能的 API 调用体验。

<a href="https://www.python.org">
  <img src="https://img.shields.io/github/languages/top/angjustinl/ASFConnector" alt="languages">
</a> 
<img src="https://img.shields.io/github/license/ANGJustinl/ASFConnector" alt="license">
<img src="https://img.shields.io/badge/python-3.12-blue.svg" alt="python">
<img src="https://img.shields.io/badge/asyncio-supported-brightgreen.svg" alt="asyncio">
<img src="https://img.shields.io/badge/ASF-6.2.2.3--latest%20supported-black.svg" alt="ASF">
<img src="https://img.shields.io/badge/code%20style-ruff-black?style=flat-square&logo=ruff" alt="ruff">
<img src="https://results.pre-commit.ci/badge/github/ANGJustinl/nonebot_plugin_archisteamfarm/master.svg" alt="pre-commit">
</div>

### [已实现 API](../API.md)

## 架构设计

### 核心组件

1. **ASFConnector** (`__init__.py`)
   - 主入口类，管理连接生命周期
   - 统一管理所有 Controller 实例
   - 支持 `async with` 上下文管理器以复用连接池

2. **IPCProtocolHandler** (`IPCProtocol.py`)
   - 底层 HTTP 客户端封装
   - 使用 `httpx.AsyncClient` 实现异步请求
   - 支持连接池复用以提升性能

3. **BaseController** (`BaseController.py`)
   - 所有 Controller 的基类
   - 提供通用的 GET/POST/DELETE 请求方法
   - 统一日志记录

4. **ASFConfig** (`config.py`)
   - 基于 Pydantic 的配置管理
   - 支持从 .env 文件加载配置
   - 自动验证配置参数

5. **Controller 模块**
   - **ASFController**: ASF 全局操作（获取信息、更新配置、重启等）
   - **BotController**: Bot 相关操作（启动、停止、兑换等）
   - **NLogController**: 日志相关操作（获取日志文件）
   - **TypeController**: 类型信息查询
   - **StructureController**: 结构信息查询
   - **CommandController**: 命令执行（已标记为遗留功能）

## 快速开始

> **⚠️ 重要提示：在 ASF 中配置默认 Bot**
>
> 在使用本库的任何 Bot 相关操作之前，您**必须**在 ASF 全局配置中配置 `DefaultBot`。如果没有此设置，所有 Bot 相关操作可能会表现出随机行为，产生与预期不符的结果。
>
> 在您的 ASF `ASF.json` 配置文件中添加以下内容：
> ```json
> {
>   "DefaultBot": "your_primary_bot_name"
> }
> ```
>
> 更多详情请参阅：[ASF 配置 - DefaultBot](https://github.com/JustArchiNET/ArchiSteamFarm/wiki/Configuration#defaultbot)

### 配置设置

1. 复制 `.env.example` 到 `.env`:
```bash
cp .env.example .env
```

2. 编辑 `.env` 文件:
```env
ASF_HOST=127.0.0.1
ASF_PORT=1242
ASF_PASSWORD=your_ipc_password
ENABLE_RICH_TRACEBACK=False
```

### 基本用法（推荐）

使用 `.env` 配置文件，自动加载配置：

```python
import asyncio
from ASFConnector import ASFConnector

async def main():
    # 从 .env 文件自动加载配置
    async with ASFConnector.from_config() as connector:
        # 获取 ASF 信息
        asf_info = await connector.asf.get_info()
        print(f"ASF Version: {asf_info['Result']['Version']}")
        
        # 获取 Bot 信息
        bot_info = await connector.bot.get_info('bot_name')
        print(bot_info)

asyncio.run(main())
```

### 使用自定义配置

```python
import asyncio
from ASFConnector import ASFConnector
from ASFConnector.config import ASFConfig

async def main():
    # 创建自定义配置
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

### 直接传参（向后兼容）

```python
import asyncio
from ASFConnector import ASFConnector

async def main():
    # 直接传参创建连接
    async with ASFConnector(
        host='127.0.0.1',
        port='1242',
        password='your_ipc_password'
    ) as connector:
        info = await connector.asf.get_info()
        print(f"Request: {info['Success']}")

asyncio.run(main())
```

## API 参考

<details>
<summary><b>ASFController</b></summary>

#### `get_info()`
获取 ASF 全局信息。

```python
info = await connector.asf.get_info()
```

**响应示例：**
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
更新 ASF 全局配置。

```python
config = {
    "AutoRestart": True,
    "UpdatePeriod": 24
}
result = await connector.asf.update_config(config)
```

#### `exit()`
关闭 ASF。

```python
result = await connector.asf.exit()
```

#### `restart()`
重启 ASF。

```python
result = await connector.asf.restart()
```

#### `update()`
更新 ASF 到最新稳定版本。

```python
result = await connector.asf.update()
```

#### `encrypt(data: dict)`
使用 ASF 加密机制加密数据。

```python
data = {
    "CryptoMethod": 0,  # 加密方法 (0 = AES)
    "StringToEncrypt": "my_sensitive_data"
}
result = await connector.asf.encrypt(data)
```

#### `hash(data: dict)`
使用 ASF 哈希机制对数据进行哈希处理。

```python
data = {
    "HashMethod": 0,  # 哈希方法 (0 = SHA256)
    "StringToHash": "my_string_to_hash"
}
result = await connector.asf.hash(data)
```

</details>

<details>
<summary><b>BotController</b></summary>

#### `get_info(bot_names: str)`
获取指定 Bot 的信息。

```python
# 单个 Bot
info = await connector.bot.get_info('bot1')

# 多个 Bot（逗号分隔）
info = await connector.bot.get_info('bot1,bot2')

# 所有 Bot
info = await connector.bot.get_info('ASF')
```

#### `start(bot_names: str)`
启动指定的 Bot。

```python
result = await connector.bot.start('bot1')
```

#### `stop(bot_names: str)`
停止指定的 Bot。

```python
result = await connector.bot.stop('bot1')
```

#### `pause(bot_names: str)`
暂停指定 Bot 的挂卡。

```python
result = await connector.bot.pause('bot1')
```

#### `resume(bot_names: str)`
恢复指定 Bot 的挂卡。

```python
result = await connector.bot.resume('bot1')
```

#### `redeem(bot_names: str, keys)`
在指定 Bot 上激活 CD-Key。

```python
# 单个 Key
result = await connector.bot.redeem('bot1', 'XXXXX-XXXXX-XXXXX')

# 多个 Key
keys = ['KEY1', 'KEY2', 'KEY3']
result = await connector.bot.redeem('bot1', keys)
```

#### `add_license(bot_names: str, licenses)`
添加免费许可证。

```python
result = await connector.bot.add_license('bot1', [12345, 67890])
```

#### `get_inventory(bot_names: str, app_id: int = None, context_id: int = None)`
获取库存信息。

```python
# 获取通用库存
inventory = await connector.bot.get_inventory('bot1')

# 获取特定游戏库存（Steam 交易卡片）
inventory = await connector.bot.get_inventory('bot1', app_id=753, context_id=6)
```

#### `input(bot_names: str, input_type: str, input_value: str)`
为 Bot 提供输入值（如 Steam 令牌）。

```python
result = await connector.bot.input('bot1', 'SteamGuard', 'ABCDE')
```

#### `rename(bot_name: str, new_name: str)`
重命名 Bot。

```python
result = await connector.bot.rename('old_bot_name', 'new_bot_name')
```

#### `delete_games_to_redeem_in_background(bot_names: str)`
删除后台游戏激活输出文件。

```python
result = await connector.bot.delete_games_to_redeem_in_background('bot1')
```

</details>

<details>
<summary><b>NLogController</b></summary>

#### `get_log_file()`
获取 ASF 日志文件内容。

```python
log_content = await connector.nlog.get_log_file()
if log_content.get('Success'):
    print(log_content['Result'])
```

#### `get_log_stream()`
获取实时日志流（需要 WebSocket 支持）。

```python
# 注意：此端点需要 WebSocket 客户端
# 当前返回提示信息，指导如何使用 WebSocket 连接
result = await connector.nlog.get_log_stream()
```

</details>

<details>
<summary><b>TypeController</b></summary>

#### `get_type(type_name: str)`
获取指定类型的类型信息。

```python
type_info = await connector.type.get_type('ArchiSteamFarm.Steam.Storage.BotConfig')
```

</details>

<details>
<summary><b>StructureController</b></summary>

#### `get_structure(structure_name: str)`
获取指定类型的默认结构。

```python
structure = await connector.structure.get_structure('ArchiSteamFarm.Storage.GlobalConfig')
```

</details>

<details>
<summary><b>CommandController (IPC API遗留功能)</b></summary>

> **注意：** 此 Controller 已被ASF官方标记为遗留功能，建议使用 ASFController 和 BotController 的特定方法。

#### `execute(command: str)`
执行命令。

```python
result = await connector.command.execute('status ASF')
```

</details>

## 配置管理

### 配置验证

ASFConfig 使用 Pydantic 进行配置验证：

```python
from ASFConnector.config import ASFConfig
from pydantic import ValidationError

try:
    config = ASFConfig(
        asf_host='127.0.0.1',
        asf_port='1242',  # 自动验证端口范围 (1-65535)
        asf_path='Api'    # 自动添加前导斜杠 -> '/Api'
    )
    config.log_config()
except ValidationError as e:
    print(f"配置验证失败: {e}")
```

### 配置参数

| 参数 | 环境变量 | 默认值 | 说明 |
|------|---------|--------|------|
| `asf_host` | `ASF_HOST` | `127.0.0.1` | ASF IPC 主机地址 |
| `asf_port` | `ASF_PORT` | `1242` | ASF IPC 端口 (1-65535) |
| `asf_password` | `ASF_PASSWORD` | `None` | ASF IPC 密码（可选） |
| `asf_path` | `ASF_PATH` | `/Api` | ASF IPC API 路径 |

## 性能优化

### 连接池复用

使用 `async with` 上下文管理器可以显著提升性能：

```python
# 不使用连接池（每次请求创建新连接）
async with ASFConnector.from_config() as connector:
    await connector.asf.get_info()  # 较慢

# 使用连接池（复用连接，推荐）
async with ASFConnector.from_config() as connector:
    for i in range(100):
        await connector.asf.get_info()  # 更快！
```

### 性能对比

根据测试结果（10次请求）：
```
Results for 10 requests:
  Legacy API (no pool):     0.109s (10.9ms per request)
  New Controller (no pool): 0.111s (11.1ms per request)
  New Controller (w/ pool): 0.004s (0.4ms per request)

Speedup with connection pool: 28.51x faster
Time saved per request: 10.7ms
```


## 错误处理

所有 API 调用都返回包含 `Success` 字段的字典：

```python
response = await connector.asf.get_info()

if response.get('Success'):
    data = response.get('Result')
    print(f"Success: {data}")
else:
    error_msg = response.get('Message', 'Unknown error')
    print(f"Error: {error_msg}")
```

当 IPC 请求触发 HTTP/网络异常时，响应字典中还会包含：

- `ExceptionType`: 对应的自定义异常类名称（例如 `ASF_NotFound`）
- `Exception`: 具体的异常实例，带有 `status_code` 与原始 `payload`
- `StatusCode`: HTTP 状态码（若可用）
- `ResponsePayload`: ASF 返回的 JSON 或纯文本内容（若可用）

库中提供了统一的异常定义，可通过 `ASFConnector` 顶层导出或 `ASFConnector.error` 模块使用：

```python
from ASFConnector import ASF_BadRequest, ASF_NotFound

response = await connector.type.get_type('ArchiSteamFarm.Storage.UnknownType')
if not response['Success']:
    exc = response['Exception']
    if isinstance(exc, ASF_NotFound):
        print("类型不存在，原始响应:", response.get('ResponsePayload'))
    else:
        raise exc  # 根据需要抛出或记录
```

所有内置异常均继承自 `ASFConnectorError`，常见 HTTP 状态与异常的映射如下：

| HTTP 状态码 | 异常类型 |
|-------------|----------|
| 400 | `ASF_BadRequest` |
| 401 | `ASF_Unauthorized` |
| 403 | `ASF_Forbidden` |
| 404 | `ASF_NotFound` |
| 405 | `ASF_NotAllowed` |
| 406 | `ASF_NotAcceptable` |
| 411 | `ASF_LengthRequired` |
| 501 | `ASF_NotImplemented` |


## 更多信息

- [ASF IPC API 文档](https://github.com/JustArchiNET/ArchiSteamFarm/wiki/IPC)
- [ASF Wiki](https://github.com/JustArchiNET/ArchiSteamFarm/wiki)

## TODO

- [ ] 添加更多单元和集成测试，以超越当前由 actions 支持的范围
- [ ] 命令行工具，用于快速操作而无需编写代码
- [ ] WebSocket 支持，用于实时日志流监控（可能）

## 许可证

本项目遵循与 [dmcallejo/ASFBot](https://github.com/dmcallejo/ASFBot) 相同的许可证。
