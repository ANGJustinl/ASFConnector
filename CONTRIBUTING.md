# Contributing to ASFConnector

Thank you for your interest in contributing to ASFConnector!

## Development Setup

### Prerequisites

- Python 3.10 or higher
- [uv](https://github.com/astral-sh/uv) package manager
- An ArchiSteamFarm (ASF) instance for integration testing (optional)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/ANGJustinl/ASFConnector.git
cd ASFConnector
```

2. Install dependencies using uv:
```bash
uv sync --group dev
```

3. Create a `.env` file for configuration (optional, for integration tests):
```bash
cp .env.example .env
# Edit .env with your ASF instance details
```

## Running Tests

### Unit Tests Only (No ASF Required)

By default, tests that require an ASF instance are skipped:

```bash
uv run poe test
```

This will run tests with coverage reporting, skipping integration tests.

### All Tests (ASF Required)

To run all tests including integration tests that require an ASF instance:

```bash
# Option 1: Using environment variable
RUN_INTEGRATION_TESTS=true uv run poe test-all

# Option 2: Using pytest flag
uv run pytest --run-integration -v
```

**Note:** Integration tests require a running ASF instance configured in your `.env` file.

### Running Specific Tests

```bash
# Run a specific test file
uv run pytest test_asfconnector.py -v

# Run a specific test
uv run pytest test_asfconnector.py::PersistenceTest::test_asf_with_context_manager -v
```

## Code Quality

### Linting and Formatting

The project uses Ruff for linting and formatting:

```bash
# Run ruff checks
ruff check .

# Fix auto-fixable issues
ruff check --fix .

# Format code
ruff format .
```

### Pre-commit Hooks

The project uses pre-commit hooks to ensure code quality:

```bash
# Install pre-commit hooks
pre-commit install

# Run manually
pre-commit run --all-files
```

## Project Structure

```
ASFConnector/
├── ASFConnector/          # Main package
│   ├── Controllers/       # API endpoint controllers
│   ├── IPCProtocol.py    # HTTP client wrapper
│   ├── config.py         # Configuration management
│   ├── error.py          # Exception definitions
│   └── __init__.py       # Main entry point
├── test_*.py             # Test files
├── conftest.py           # Pytest configuration
├── pyproject.toml        # Project configuration
└── uv.lock              # Dependency lock file
```

## Making Changes

1. Create a new branch for your feature/fix:
```bash
git checkout -b feature/your-feature-name
```

2. Make your changes and write tests

3. Run tests and linting:
```bash
uv run poe test
ruff check .
ruff format .
```

4. Commit your changes with clear messages:
```bash
git commit -m "feat: add ASF connection timeout handling"
```

5. Push and create a pull request

## Testing Strategy

- **Unit Tests**: Test individual components in isolation (do not require ASF)
- **Integration Tests**: Test interaction with a real ASF instance (marked with `@pytest.mark.integration`)

Integration tests are automatically marked and skipped unless:
- The `--run-integration` flag is provided to pytest
- The `RUN_INTEGRATION_TESTS=true` environment variable is set

## CI/CD

The project uses GitHub Actions for continuous integration:

- **CI Workflow**: Runs on push to master and pull requests
  - Typo checking
  - Unit tests across Python 3.10-3.13 and multiple OS
  - Code coverage reporting to Codecov
  - Integration tests are skipped in CI by default

- **Release Workflow**: Triggered on version tags
  - Builds distribution packages
  - Publishes to PyPI
  - Creates GitHub releases

## Questions?

If you have questions, please open an issue on GitHub.
