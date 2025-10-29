"""
Simple test script for TypeController and StructureController
"""

import asyncio

from ASFConnector import ASFConnector


async def test_type_structure_controllers():
    """Test TypeController and StructureController endpoints"""

    # Initialize connector (update with your ASF settings)
    async with ASFConnector().from_config() as connector:
        # Test 1: Get type information
        test_types = [
            "ArchiSteamFarm.Steam.Storage.BotConfig",
            "ArchiSteamFarm.Storage.GlobalConfig",
        ]

        for type_name in test_types:
            try:
                result = await connector.type.get_type(type_name)
                if result.get("Success"):
                    # Show a preview of the result
                    result_data = result.get("Result", {})
                    if isinstance(result_data, dict):
                        pass
                    else:
                        pass
                else:
                    pass
            except Exception:
                pass

        # Test 2: Get structure information
        test_structures = [
            "ArchiSteamFarm.Steam.Storage.BotConfig",
            "ArchiSteamFarm.Storage.GlobalConfig",
        ]

        for structure_name in test_structures:
            try:
                result = await connector.structure.get_structure(structure_name)
                if result.get("Success"):
                    # Show a preview of the result
                    result_data = result.get("Result", {})
                    if isinstance(result_data, dict):
                        # Show first few properties
                        for i, key in enumerate(list(result_data.keys())[:3]):
                            pass
                        if len(result_data) > 3:
                            pass
                    else:
                        pass
                else:
                    pass
            except Exception:
                pass


if __name__ == "__main__":
    asyncio.run(test_type_structure_controllers())
