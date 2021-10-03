# overview

## Packages
 - use [geoiplookup](http://geoiplookup.net/xml-api/) for geoip, no ratelimit mentioned
 - use [rdap.org](https://about.rdap.org/) for rdap lookups, ratelimit: 10 per second, also need to follow redirects


 - use [redis](https://redis.io/) for in memory caching and saving of items
 - use [redis-py](https://github.com/andymccurdy/redis-py) to communicate to redis from python


 - use [docker](https://www.docker.com/) to have easy start configurations and cleanup


 - use [python unittest](https://docs.python.org/3/library/unittest.html) to do unit tests as it is based on JUnit and is in the python standard lib
 - use [python typing](https://docs.python.org/3/library/typing.html) to do type hinting, in python >3.5
 - use [python requests](https://pypi.org/project/requests/) to do http requests

## Structure

Each section will be split into a separate module, (parse, geoip, RDAP, cache)

The command line util will have separate steps, each part will be saved to the redis database

There will be a config file for each service with rate limits (geoip and rdap)