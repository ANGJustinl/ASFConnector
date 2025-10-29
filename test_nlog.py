"""
Simple test script for NLogController
"""

import asyncio

from ASFConnector import ASFConnector


async def test_nlog_controller():
    """Test NLogController endpoints"""

    # Initialize connector (update with your ASF settings)
    async with ASFConnector().from_config() as connector:
        # Test 1: Get log file
        try:
            result = await connector.nlog.get_log_file()
            if result.get("Success"):
                # Log content might be large, so just show first 200 chars
                log_content = result.get("Result", "")
                if isinstance(log_content, str):
                    pass
                else:
                    pass
            else:
                pass
        except Exception:
            pass

        # Test 2: Get log stream (WebSocket endpoint)
        result = await connector.nlog.get_log_stream()
        if result.get("Success"):
            pass
        else:
            pass


if __name__ == "__main__":
    asyncio.run(test_nlog_controller())
