# ip-search-python-challenge
Challenge to find geoIP and RDAP lookups in python

# Setup
You will need these installed:
`docker, postgresql, redis`

 - Sign up for [geoIP2Lite](https://www.maxmind.com/en/geolite2/signup?lang=en) and grab a license key
 - Put your license key into a file named `config.cfg` in the `setup/` folder, with the format:

```
geoIPUsername=<your username here>
geoIPApiKey=<your api key here>
localDatabasePassword=<random password here>
```

`cd` into `setup/`
and run `bash install-geoip2lite-database.sh` 

##### NOTE: if you get container already in use (like from a previous run of this script) `bash delete-containers.sh` will remove the containers made in this setup script

`cd` to the main folder and run:
```
python3 -m venv ./venv/
source venv/bin/activate
python3 -m pip install -r requirements.txt
```
(use `deactivate` to leave the python virtual environment)

# Usage
If you want the full cli command tree see [this](https://github.com/eatthoselemons/ip-search-python-challenge/blob/main/notes/cli-plan.yml)
##### NOTE: you can also just use --help on `python3 main.py` to get further information. example: `python3 main.py locate --help`

## Basics
 - `python3 main.py parse <file with ips>`
 - `python3 main.py locate`
 - `python3 main.py whos`

Those commands will read in a file that has ip's, parse it, do the geoip lookup and the RDAP lookups

##### NOTE: There are intermediate files between each command, if you want to save the data somewhere look at those (`ipList.txt`, `geoIPs.txt`, `rdapIPs.txt` are the defaults)

If you have a specific ip you want to search for try `python3 main.py search <ip>` if you have gotten the information before with `locate` or `whos` then you will get that printed out

# Things to Improve
 - Make `GeoIPDatabaseService` and `GeoIPApiService` implement the `GeoIPService` interface
 - Do validation of the api data and http response codes
 - Reduce repeated code for `find_data()`
 - Get to 100% code coverage
