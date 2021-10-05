# ip-search-python-challenge
Challenge to find geoIP and RDAP lookups in python

# setup
You will need these installed:
`docker, postgresql, redis`

 - Sign up for [geoIP2Lite](https://www.maxmind.com/en/geolite2/signup?lang=en) and grab a license key
 - Put your license key into a file named `config.cfg` in the format:

```
geoIPUsername=<your username here>
geoIPLicenseKey=<your api key here>
localDatabasePassword=<random password here>
```

run `bash install-geoip2lite-database.sh` 
