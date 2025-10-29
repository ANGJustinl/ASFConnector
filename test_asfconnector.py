import unittest
import asyncio
import time
from ASFConnector import ASFConnector


class PersistenceTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.conn = ASFConnector().from_config()

    # Test with context manager (connection pool reuse)
    def test_asf_with_context_manager(self):
        """Test using ASFConnector with context manager for connection pool reuse"""

        async def run_test():
            async with ASFConnector().from_config() as conn:
                info = await conn.asf.get_info()
                assert info["Success"] is True

                # Multiple requests should reuse the same connection
                info2 = await conn.bot.get_info("ANG2")
                assert info2["Success"] is True

                info3 = await conn.bot.get_inventory("ANG2")
                assert info3["Success"] is True

        asyncio.run(run_test())

    # Legacy API tests (only run for performance comparison)
    @unittest.skip("Legacy tests - use test_performance_comparison to compare")
    def test_get_asf_info_legacy(self):
        """Test legacy get_asf_info method"""
        info = asyncio.run(self.conn.get_asf_info())
        assert info["Success"] is True

    @unittest.skip("Legacy tests - use test_performance_comparison to compare")
    def test_get_bot_info_legacy(self):
        """Test legacy get_bot_info method"""
        result = asyncio.run(self.conn.get_bot_info("1"))
        assert isinstance(result, str)

    @unittest.skip("Legacy tests - use test_performance_comparison to compare")
    def test_send_command_legacy(self):
        """Test legacy send_command method"""
        result = asyncio.run(self.conn.send_command("help"))
        assert isinstance(result, str)

    # Performance comparison tests (includes legacy methods)
    @unittest.skipUnless(False, "Performance test - set to True to run")
    def test_performance_comparison(self):
        """Compare performance: legacy vs new API vs connection pool"""
        print("\n" + "=" * 60)
        print("Performance Comparison Test")
        print("=" * 60)

        num_requests = 10

        # Test 1: Legacy method without connection pool
        async def test_legacy_no_pool():
            conn = ASFConnector().from_config()
            start = time.time()
            for _ in range(num_requests):
                await conn.get_asf_info()
            elapsed = time.time() - start
            return elapsed

        # Test 2: New Controller API without connection pool
        async def test_new_no_pool():
            conn = ASFConnector().from_config()
            start = time.time()
            for _ in range(num_requests):
                await conn.asf.get_info()
            elapsed = time.time() - start
            return elapsed

        # Test 3: New Controller API WITH connection pool
        async def test_new_with_pool():
            async with ASFConnector().from_config() as conn:
                start = time.time()
                for _ in range(num_requests):
                    await conn.asf.get_info()
                elapsed = time.time() - start
                return elapsed

        legacy_time = asyncio.run(test_legacy_no_pool())
        new_time = asyncio.run(test_new_no_pool())
        pool_time = asyncio.run(test_new_with_pool())

        print(f"\nResults for {num_requests} requests:")
        print(
            f"  Legacy API (no pool):     {legacy_time:.3f}s ({legacy_time / num_requests * 1000:.1f}ms per request)"
        )
        print(
            f"  New Controller (no pool): {new_time:.3f}s ({new_time / num_requests * 1000:.1f}ms per request)"
        )
        print(
            f"  New Controller (w/ pool): {pool_time:.3f}s ({pool_time / num_requests * 1000:.1f}ms per request)"
        )
        print(f"\nSpeedup with connection pool: {(new_time / pool_time):.2f}x faster")
        print(
            f"Time saved per request: {(new_time - pool_time) / num_requests * 1000:.1f}ms"
        )
        print("=" * 60)

        # Assert that connection pool is faster
        assert pool_time < new_time, (
            "Connection pool should be faster than without pool"
        )


if __name__ == "__main__":
    unittest.main()
