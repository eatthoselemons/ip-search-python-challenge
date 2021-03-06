  unzip geoIP2Lite.zip
trap_msg='s=${?}; echo "${0}: Error on line "${LINENO}": ${BASH_COMMAND}"; exit ${s}'
set -uo pipefail
trap "${trap_msg}" ERR

# source my config bash lib
source ./config.shlib

# read config file
licenseKey=$(getConfigVar config.cfg geoIPApiKey)
password=$(getConfigVar config.cfg localDatabasePassword)

export PGPASSWORD=$password

# download the csv's
mkdir -p geoIP
echo "downloading the csv's..."
if [ ! -f geoIP/geoIP2Lite.zip ]; then
  curl -L -o geoIP/geoIP2Lite.zip "https://download.maxmind.com/app/geoip_download?edition_id=GeoLite2-City-CSV&license_key=${licenseKey}&suffix=zip"
fi
cd geoIP
unzip -o geoIP2Lite.zip
cd GeoLite2-City-CSV_*
pwd

# setup and run postgres docker container
echo "starting postgres docker container"
docker run --name postgres-db-geoip -e POSTGRES_PASSWORD=$password -p 5432:5432 -d postgres

# should be waiting don't know why
#until [ "`docker inspect -f {{.State.Running}} postgres-db`"=="true" ]; do
#    sleep 0.1;
#done;

sleep 10

# creating the db for the data
echo "creating database"
createdb -h localhost -U postgres -p 5432 -T template0 geoip

# import geolite into postgres
echo "importing block csv's..."
psql -h localhost -U postgres -d geoip -c "create table geoip2_network (
  network cidr not null,
  geoname_id int,
  registered_country_geoname_id int,
  represented_country_geoname_id int,
  is_anonymous_proxy bool,
  is_satellite_provider bool,
  postal_code text,
  latitude numeric,
  longitude numeric,
  accuracy_radius int
);"

# ipv4
psql -h localhost -U postgres -d geoip -c "\\copy geoip2_network(
  network, geoname_id, registered_country_geoname_id, represented_country_geoname_id,
  is_anonymous_proxy, is_satellite_provider, postal_code, latitude, longitude, accuracy_radius
) from 'GeoLite2-City-Blocks-IPv4.csv' with (format csv, header);"

# ipv6
psql -h localhost -U postgres -d geoip -c "\\copy geoip2_network(
  network, geoname_id, registered_country_geoname_id, represented_country_geoname_id,
  is_anonymous_proxy, is_satellite_provider, postal_code, latitude, longitude, accuracy_radius
) from 'GeoLite2-City-Blocks-IPv6.csv' with (format csv, header);"

psql -h localhost -U postgres -d geoip -c "create index on geoip2_network using gist (network inet_ops);"

echo "importing city csv..."
psql -h localhost -U postgres -d geoip -c "create table geoip2_location (
  geoname_id int not null,
  locale_code text not null,
  continent_code text not null,
  continent_name text not null,
  country_iso_code text,
  country_name text,
  subdivision_1_iso_code text,
  subdivision_1_name text,
  subdivision_2_iso_code text,
  subdivision_2_name text,
  city_name text,
  metro_code int,
  time_zone text,
  is_in_european_union bool not null,
  primary key (geoname_id, locale_code)
);"

psql -h localhost -U postgres -d geoip -c "\\copy geoip2_location(
  geoname_id, locale_code, continent_code, continent_name, country_iso_code, country_name,
  subdivision_1_iso_code, subdivision_1_name, subdivision_2_iso_code, subdivision_2_name,
  city_name, metro_code, time_zone, is_in_european_union
) from 'GeoLite2-City-Locations-en.csv' with (format csv, header);"

echo "finished installing postgres"

# setting up redis
echo "starting redis docker container"
docker run --name redis-geoip -p 6379:6379 -d redis

# clear the password
export PGPASSWORD=""
