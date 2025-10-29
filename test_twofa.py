"""
Test script for TwoFactorAuthenticationController
"""

import asyncio

from ASFConnector import ASFConnector


async def test_twofa():
    """Test 2FA token retrieval"""

    # Initialize connector from .env
    async with ASFConnector.from_config() as connector:
        # Test: Get 2FA tokens for all bots

        try:
            result = await connector.twofa.get_token("ASF")

            if result.get("Success"):
                if "Result" in result:
                    len(result["Result"])

                    for bot, token_data in result["Result"].items():
                        if token_data.get("Success"):
                            token_data.get("Result", "N/A")
                        else:
                            token_data.get("Message", "Unknown error")
                else:
                    pass
            else:
                result.get("Message", "Unknown error")

        except Exception:
            pass

        # Test 3: Health check
        try:
            health = await connector.health_check()
            if health.get("Success"):
                pass
            else:
                pass
        except Exception:
            pass


if __name__ == "__main__":
    asyncio.run(test_twofa())
