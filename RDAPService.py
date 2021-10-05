import time
import redis
import json
import requests


class RDAPService:
    def __init__(self):
        self.r = redis.Redis(host='localhost', port=6379, db=0)

    def find_data(self, ip: str, use_cache: bool) -> json:
        if use_cache:
            return self.r.get(ip) or self.jsonify_api(ip)
        else:
            return self.jsonify_api(ip)

    # remember to check if the http header is correct if not throw
    def jsonify_api(self, ip: str) -> json:
        r = requests.get(f'https://rdap.org/ip/{ip}')
        time.sleep(0.2)

        return json.dumps(r.text)
