import psycopg
import redis
from psycopg.rows import dict_row
import json


class GeoIPDatabaseService:
    def __init__(self, **kwargs):
        self.r = redis.Redis(host='localhost', port=6379, db=0)
        self.postgres_password = kwargs['localDatabasePassword']

    def find_data(self, ip: str, use_cache: bool) -> json:
        if use_cache:
            return self.r.get(ip) or self.jsonify_database(ip)
        else:
            return self.jsonify_database(ip)

    def jsonify_database(self, ip: str) -> json:
        with psycopg.connect(dbname='geoip', user='postgres',
                             password=self.postgres_password,
                             host='localhost', port='5432', row_factory=dict_row) as conn:
            geoip_id = conn.execute(f"select geoname_id from geoip2_network where network >> '{ip}';").fetchone()
            row = conn.execute(f"select * from geoip2_location where geoname_id={geoip_id['geoname_id']};").fetchone()

        return json.dumps(row)
