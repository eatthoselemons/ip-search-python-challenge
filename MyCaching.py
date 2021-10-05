import json
import redis


class MyCaching:
    def __init__(self):
        self.r = redis.Redis(host='localhost', port=6379, db=0)

    def put_in_cache(self, ip: str, found_data: json):
        self.r.set(ip, found_data)
        return found_data
