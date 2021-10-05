import redis
import requests
import json


class GeoIPApiService:
    def __init__(self, **kwargs):
        self.r = redis.Redis(host='localhost', port=6379, db=0)
        self.geoip_api_username = kwargs['geoIPUsername']
        self.geoip_api_key = kwargs['geoipApiKey']

    def find_data(self, ip: str, use_cache: bool) -> json:
        """Finds the data if use_cache is true then checks the redis database before the api"""
        if use_cache:
            return self.r.get(ip).decode('utf-8') or self.jsonify_api(ip)
        else:
            return self.jsonify_api(ip)

    # remember to check if the http header is correct if not throw
    def jsonify_api(self, ip: str) -> json:
        request = requests.get(f"https://geolite.info/geoip/v2.1/city/{ip}",
                               auth=(self.geoip_api_username, self.geoip_api_key))
        if not request.status_code == requests.codes.ok:
            return request.text
        else:
            request.raise_for_status()
