# ASFConnector 测试文档

本目录包含 ASFConnector 项目的所有测试代码。

## 测试结构

```
tests/
├── conftest.py              # Pytest配置和共享fixtures
├── test_config.py          # 配置管理测试
├── test_asfconnector.py    # 核心功能测试
├── test_controllers.py     # Controllers测试
├── test_errors.py          # 错误处理测试
├── .env.test               # 测试环境配置
└── README.md               # 本文件
```

## 运行测试

### 使用 uv（推荐）

```bash
# 运行所有测试
uv run poe test

# 或直接使用pytest
uv run pytest

# 运行特定测试文件
uv run pytest tests/test_config.py

# 运行特定测试类或函数
uv run pytest tests/test_config.py::TestASFConfig::test_default_config

# 显示详细输出
uv run pytest -v

# 显示print输出
uv run pytest -s

# 生成覆盖率报告
uv run pytest --cov=ASFConnector --cov-report=html
```

### 使用传统方式

```bash
# 安装测试依赖
pip install -e ".[test]"

# 运行测试
pytest

# 生成覆盖率报告
pytest --cov=ASFConnector --cov-report=xml --cov-report=html
```

## 测试配置

### 环境变量

测试使用以下环境变量（可在 `.env.test` 中配置）：

- `ASF_HOST`: ASF服务器地址（默认: 127.0.0.1）
- `ASF_PORT`: ASF服务器端口（默认: 1242）
- `ASF_PASSWORD`: ASF IPC密码（测试用）
- `ASF_PATH`: API路径（默认: /Api）
- `ENVIRONMENT`: 环境标识（应设为 test）

### Pytest 配置

在 `pyproject.toml` 中配置了以下选项：

- **异步测试**: 使用 `pytest-asyncio` 自动处理
- **并行测试**: 使用 `pytest-xdist` 支持 `-n auto`
- **覆盖率**: 使用 `pytest-cov` 生成覆盖率报告
- **详细输出**: 默认启用 `-v` 和 `-s`

## 测试类别

### 1. 配置测试 (`test_config.py`)

测试 ASFConfig 类的配置管理功能：
- 默认配置值
- 自定义配置
- 参数验证（主机、端口、路径）
- 环境变量加载
- 配置日志输出

### 2. 核心功能测试 (`test_asfconnector.py`)

测试 ASFConnector 主类：
- 初始化（多种方式）
- 上下文管理器
- 健康检查
- 连接池复用
- 向后兼容方法

### 3. Controller测试 (`test_controllers.py`)

测试各个 Controller 类：
- ASFController: ASF全局操作
- BotController: Bot相关操作
- CommandController: 命令执行
- NLogController: 日志操作
- TypeController: 类型查询
- StructureController: 结构查询

### 4. 错误处理测试 (`test_errors.py`)

测试异常处理机制：
- 异常类层次结构
- HTTP状态码映射
- 错误信息提取
- 异常转换和传播

## Fixtures说明

### `mock_asf_config`
提供模拟的ASF配置字典。

### `mock_asf_responses`
提供常见ASF API响应的模拟数据。

### `mock_httpx_client`
提供模拟的httpx.AsyncClient实例。

### `mock_ipc_handler`
提供模拟的IPCProtocolHandler实例。

### `mock_asf_connector`
提供完整的模拟ASFConnector实例（不进行真实网络调用）。

## CI/CD 集成

### GitHub Actions

测试会在以下情况自动运行：
- Push到master分支
- 提交Pull Request
- 修改源代码或测试文件

工作流配置位于 `.github/workflows/ci.yml`。

### 测试矩阵

测试在以下环境中运行：
- Python版本: 3.10, 3.11, 3.12, 3.13
- 操作系统: Ubuntu, Windows, macOS

### 覆盖率报告

测试覆盖率会自动上传到 Codecov：
- 单元测试结果上传
- 覆盖率报告生成
- PR中显示覆盖率变化

## 编写新测试

### 基本结构

```python
import pytest
from ASFConnector import ASFConnector

class TestYourFeature:
    """Test your feature."""
    
    def test_something(self):
        """Test something specific."""
        # Arrange
        connector = ASFConnector()
        
        # Act
        result = connector.do_something()
        
        # Assert
        assert result is not None
    
    @pytest.mark.asyncio
    async def test_async_feature(self, mock_asf_connector):
        """Test async feature."""
        async with mock_asf_connector as connector:
            result = await connector.asf.get_info()
            assert result["Success"] is True
```

### 使用Mock

```python
from unittest.mock import patch, AsyncMock

@pytest.mark.asyncio
async def test_with_mock(self, mock_asf_connector):
    """Test with mocked responses."""
    mock_response = {"Success": True, "Result": {}}
    
    with patch.object(
        mock_asf_connector.asf, 
        "get_info", 
        return_value=mock_response
    ):
        result = await mock_asf_connector.asf.get_info()
        assert result["Success"] is True
```

## 故障排查

### 导入错误

如果遇到导入错误，确保：
1. 已安装测试依赖: `uv sync --group test`
2. PYTHONPATH包含项目根目录
3. 使用正确的导入路径

### 异步测试问题

确保：
1. 使用 `@pytest.mark.asyncio` 装饰器
2. 测试函数是 `async def`
3. 使用 `await` 调用异步函数

### Mock问题

如果mock不工作：
1. 检查mock对象的路径是否正确
2. 确保在正确的位置patch
3. 验证返回值类型匹配

## 最佳实践

1. **独立性**: 每个测试应该独立运行，不依赖其他测试
2. **清晰命名**: 使用描述性的测试名称
3. **单一职责**: 每个测试只测试一个功能点
4. **使用fixtures**: 复用测试设置代码
5. **Mock外部依赖**: 避免真实的网络请求
6. **测试边界条件**: 包括正常情况和异常情况
7. **文档化**: 添加清晰的docstring说明测试目的

## 参考资源

- [Pytest文档](https://docs.pytest.org/)
- [pytest-asyncio文档](https://pytest-asyncio.readthedocs.io/)
- [pytest-cov文档](https://pytest-cov.readthedocs.io/)
- [ASFConnector文档](../README.md)