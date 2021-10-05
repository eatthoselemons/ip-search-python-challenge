from unittest import TestCase
from MyCaching import MyCaching
import redis
import json


class TestMyCaching(TestCase):
    def setUp(self) -> None:
        self.r = redis.Redis(host='localhost', port=6379, db=0)

    def test_put_in_cache(self):
        my_cache = MyCaching()
        my_cache.put_in_cache('put_in_cache', "test string")
        saved_value = self.r.get('put_in_cache').decode("utf-8")
        self.assertEqual(saved_value, "test string")

    def test_put_in_cache_ip(self):
        my_cache = MyCaching()
        my_cache.put_in_cache('10.0.1.2', "test string")
        saved_value = self.r.get('10.0.1.2').decode("utf-8")
        self.assertEqual(saved_value, "test string")

    def tearDown(self):
        self.r.flushdb()

