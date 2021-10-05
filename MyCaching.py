import json
import redis


class MyCaching:
    def __init__(self):
        self.r = redis.Redis(host='localhost', port=6379, db=0)

    def put_in_cache(self, ip: str, found_data: str):
        """Sort of wrapper function, just puts data into the redis database then passes it on"""
        self.r.set(ip, found_data)
        return found_data
