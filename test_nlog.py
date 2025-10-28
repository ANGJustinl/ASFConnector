"""
Simple test script for NLogController
"""
import asyncio
from ASFConnector import ASFConnector

async def test_nlog_controller():
    """Test NLogController endpoints"""
    
    # Initialize connector (update with your ASF settings)
    async with ASFConnector().from_config() as connector:
        
        print("Testing NLogController...")
        print("-" * 50)
        
        # Test 1: Get log file
        print("\n1. Testing GET /Api/NLog/File (get log file)")
        try:
            result = await connector.nlog.get_log_file()
            if result.get('Success'):
                print("✓ Log file retrieved successfully")
                # Log content might be large, so just show first 200 chars
                log_content = result.get('Result', '')
                if isinstance(log_content, str):
                    print(f"  Preview: {log_content[:200]}...")
                else:
                    print(f"  Result: {result}")
            else:
                print(f"✗ Failed: {result.get('Message', 'Unknown error')}")
        except Exception as e:
            print(f"✗ Exception: {e}")
        
        # Test 2: Get log stream (WebSocket endpoint)
        print("\n2. Testing GET /Api/NLog (WebSocket for real-time logs)")
        result = await connector.nlog.get_log_stream()
        if result.get('Success'):
            print("✓ Response received")
            print(f"  Result: {result}")
        else:
            print(f"ℹ Info: {result.get('Message', 'WebSocket connection required')}")
            print("  This endpoint requires a WebSocket client for real-time log streaming.")
        
        print("\n" + "-" * 50)
        print("Test completed!")

if __name__ == '__main__':
    asyncio.run(test_nlog_controller())