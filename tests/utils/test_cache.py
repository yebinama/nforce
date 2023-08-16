from unittest.case import TestCase
import time

from nforce.utils.cache import lru_cache_ttl


class TestCache(TestCase):
    def test_lru_cache_ttl(self):
        """Test function lru_cache_ttl"""
        cached_time = lru_cache_ttl()(time.time)
        self.assertEqual(cached_time(), cached_time())

    def test_lru_cache_ttl_expires(self):
        """Test function lru_cache_ttl"""
        cached_time = lru_cache_ttl(ttl=1)(time.time)
        time1 = cached_time()
        time.sleep(1)
        self.assertNotEqual(time1, cached_time())
