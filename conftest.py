"""Pytest configuration file."""

import os
import pytest


def pytest_configure(config):
    """Configure custom markers."""
    config.addinivalue_line(
        "markers",
        "integration: marks tests as integration tests requiring ASF instance",
    )


def pytest_collection_modifyitems(config, items):
    """Automatically mark tests that use ASFConnector as integration tests."""
    for item in items:
        # Check if test file contains tests that need ASF connection
        if any(marker in str(item.nodeid) for marker in ["test_asfconnector.py", "test_nlog.py", "test_twofa.py", "test_type_structure.py"]):
            # Skip marking tests that are already skipped
            if not any(marker.name == "skip" for marker in item.iter_markers()):
                item.add_marker(pytest.mark.integration)


def pytest_addoption(parser):
    """Add custom command line options."""
    parser.addoption(
        "--run-integration",
        action="store_true",
        default=False,
        help="run integration tests that require ASF instance",
    )


def pytest_runtest_setup(item):
    """Skip integration tests unless explicitly enabled."""
    if "integration" in [marker.name for marker in item.iter_markers()]:
        if not item.config.getoption("--run-integration"):
            # Check if ASF_HOST environment variable is set and not default
            asf_host = os.environ.get("ASF_HOST", "127.0.0.1")
            run_integration = os.environ.get("RUN_INTEGRATION_TESTS", "false").lower() == "true"
            
            if not run_integration:
                pytest.skip("Integration test requires --run-integration flag or RUN_INTEGRATION_TESTS=true")
