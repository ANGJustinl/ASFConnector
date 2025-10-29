"""
Test script for TwoFactorAuthenticationController
"""

import asyncio
from ASFConnector import ASFConnector


async def test_twofa():
    """Test 2FA token retrieval"""

    print("Testing TwoFactorAuthenticationController")
    print("=" * 60)

    # Initialize connector from .env
    async with ASFConnector.from_config() as connector:
        # Test: Get 2FA tokens for all bots
        print("\nTesting GET /Api/Bot/ASF/TwoFactorAuthentication/Token (all bots)")

        try:
            result = await connector.twofa.get_token("ASF")

            if result.get("Success"):
                print("✓ Successfully retrieved 2FA tokens for all bots")

                if "Result" in result:
                    bot_count = len(result["Result"])
                    print(f"  Found {bot_count} bot(s) with 2FA")

                    for bot, token_data in result["Result"].items():
                        if token_data.get("Success"):
                            token = token_data.get("Result", "N/A")
                            print(f"    {bot}: {token}")
                        else:
                            error = token_data.get("Message", "Unknown error")
                            print(f"    {bot}: ✗ {error}")
                else:
                    print(f"  Result: {result}")
            else:
                error_msg = result.get("Message", "Unknown error")
                print(f"✗ Failed: {error_msg}")

        except Exception as e:
            print(f"✗ Exception: {e}")

        # Test 3: Health check
        print("\nTesting health check")
        try:
            health = await connector.health_check()
            if health.get("Success"):
                print(f"✓ Health check passed: {health.get('Message', 'OK')}")
            else:
                print(f"⚠ Health check warning: {health.get('Message', 'Unknown')}")
        except Exception as e:
            print(f"✗ Health check exception: {e}")

    print("\n" + "=" * 60)
    print("Test completed!")
    print("\nNote: If 2FA tokens are not available, make sure:")
    print("  1. ASF 2FA module is enabled on your bots")
    print("  2. Mobile authenticator is configured")
    print("  3. Bot names are correct")


if __name__ == "__main__":
    asyncio.run(test_twofa())
