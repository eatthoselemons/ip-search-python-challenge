import redis
import json


class GeoIPApiService:
    def __init__(self, **kwargs):
        self.r = redis.Redis(host='localhost', port=6379, db=0)
        self.api_username = kwargs['geoipUsername']
        self.geoip_api_key = kwargs['geoipApiKey']

    def find_data(self, ip: str, use_cache: bool) -> json:
        if use_cache:
            return self.r.get(ip) or self.jsonify_api(ip)
        else:
            return self.jsonify_api(ip)

    # remember to check if the http header is correct if not throw
    def jsonify_api(self, ip: str) -> json:

        return json.dumps(data)