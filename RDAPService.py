import time
import redis
import json
import requests


class RDAPService:
    def __init__(self):
        self.r = redis.Redis(host='localhost', port=6379, db=0)

    def find_data(self, ip: str, use_cache: bool) -> json:
        """Gets data for an ip. If use_cache is True then checks the redis database for the data first"""
        if use_cache:
            redis_return = self.r.get(ip)
            if redis_return:
                return redis_return.decode('utf-8')
            else:
                return self.jsonify_api(ip)
        else:
            return self.jsonify_api(ip)

    # remember to check if the http header is correct if not throw
    def jsonify_api(self, ip: str) -> json:
        r = requests.get(f'https://rdap.org/ip/{ip}')
        time.sleep(0.2)

        return r.text
