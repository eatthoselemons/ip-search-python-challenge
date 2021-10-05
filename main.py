import redis
import requests
import typer
from MyParser import MyParser
from MyWriter import MyWriter
from MyCaching import MyCaching
from RDAPService import RDAPService
from GeoIPDatabaseService import GeoIPDatabaseService
from GeoIPApiService import GeoIPApiService

app = typer.Typer()


@app.command()
def parse(input_file: str,
          output_file: str = "ipList.txt"):
    """Extracts ip's from a text file and then puts those ip's in their own file"""
    my_parser: MyParser = MyParser()
    my_writer: MyWriter = MyWriter()
    my_writer.write_ip_list(my_parser.parse_input_file(input_file), output_file)


@app.command()
def locate(input_file: str = "ipList.txt",
           output_file: str = "geoIPs.txt",
           use_cache: bool = True,
           local_database: bool = True):
    """Searches geoip based on a list of ip's in the input file.
    Depending on options will use the geoip database or the geoip api"""
    my_parser: MyParser = MyParser()
    my_caching: MyCaching = MyCaching()
    my_writer: MyWriter = MyWriter()
    config = my_parser.parse_config()
    ip_list = my_parser.parse_ip_file(input_file)
    data = {}

    # both GeoIPDatabaseService and GeoIPApiService implement the
    # interface for GeoIPService however I don't know how to add interfaces
    if local_database:
        location_service = GeoIPDatabaseService(**config)
    else:
        location_service = GeoIPApiService(**config)

    for ip in ip_list:
        try:
            data[ip] = my_caching.put_in_cache(f'geoip-{ip}', location_service.find_data(ip, use_cache))
        except requests.HTTPError:
            print("ran out of api requests saving work to file and exiting, try using the database option")
            my_writer.write_data_list(data, output_file, 'locate')
    my_writer.write_data_list(data, output_file, 'locate')


@app.command()
def whos(input_file: str = "ipList.txt",
         output_file: str = "rdapIPs.txt",
         use_cache: bool = True):
    """Checks RDAP data based on an input file with a list of ip's"""
    my_parser: MyParser = MyParser()
    my_caching: MyCaching = MyCaching()
    my_writer: MyWriter = MyWriter()
    rdap_service: RDAPService = RDAPService()
    ip_list = my_parser.parse_ip_file(input_file)
    data = {}

    for ip in ip_list:
        data[ip] = my_caching.put_in_cache(f'rdap-{ip}', rdap_service.find_data(ip, use_cache))
    my_writer.write_data_list(data, output_file, 'whos')


@app.command()
def search(ip: str):
    """Search the local redis database for an ip and print the data"""
    r = redis.Redis(host='localhost', port=6379, db=0)
    print(f"geoip data: {r.get(f'geoip-{ip}').decode('utf-8')}")
    print(f"RDAP data: {r.get(f'rdap-{ip}').decode('utf-8')}")


if __name__ == "__main__":
    app()
