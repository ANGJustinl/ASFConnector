"""
Simple test script for TypeController and StructureController
"""

import asyncio
from ASFConnector import ASFConnector


async def test_type_structure_controllers():
    """Test TypeController and StructureController endpoints"""

    # Initialize connector (update with your ASF settings)
    async with ASFConnector(
        host="127.0.0.1",
        port="21242",
        password="Angasf114",  # Replace with your actual password
    ) as connector:
        print("Testing TypeController and StructureController...")
        print("-" * 50)

        # Test 1: Get type information
        print("\n1. Testing GET /Api/Type/{type}")
        test_types = [
            "ArchiSteamFarm.Steam.Storage.BotConfig",
            "ArchiSteamFarm.Storage.GlobalConfig",
        ]

        for type_name in test_types:
            print(f"\n  Testing type: {type_name}")
            try:
                result = await connector.type.get_type(type_name)
                if result.get("Success"):
                    print("  ✓ Type information retrieved successfully")
                    # Show a preview of the result
                    result_data = result.get("Result", {})
                    if isinstance(result_data, dict):
                        print(f"    Fields count: {len(result_data.get('Body', []))}")
                    else:
                        print(f"    Result: {str(result_data)[:100]}...")
                else:
                    print(f"  ✗ Failed: {result.get('Message', 'Unknown error')}")
            except Exception as e:
                print(f"  ✗ Exception: {e}")

        # Test 2: Get structure information
        print("\n2. Testing GET /Api/Structure/{structure}")
        test_structures = [
            "ArchiSteamFarm.Steam.Storage.BotConfig",
            "ArchiSteamFarm.Storage.GlobalConfig",
        ]

        for structure_name in test_structures:
            print(f"\n  Testing structure: {structure_name}")
            try:
                result = await connector.structure.get_structure(structure_name)
                if result.get("Success"):
                    print("  ✓ Structure information retrieved successfully")
                    # Show a preview of the result
                    result_data = result.get("Result", {})
                    if isinstance(result_data, dict):
                        print(f"    Properties count: {len(result_data)}")
                        # Show first few properties
                        for i, key in enumerate(list(result_data.keys())[:3]):
                            print(f"      - {key}: {result_data[key]}")
                        if len(result_data) > 3:
                            print(
                                f"      ... and {len(result_data) - 3} more properties"
                            )
                    else:
                        print(f"    Result: {str(result_data)[:100]}...")
                else:
                    print(f"  ✗ Failed: {result.get('Message', 'Unknown error')}")
            except Exception as e:
                print(f"  ✗ Exception: {e}")

        print("\n" + "-" * 50)
        print("Test completed!")


if __name__ == "__main__":
    asyncio.run(test_type_structure_controllers())
