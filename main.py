import redis
import typer
import MyCaching
import MyParser
import MyWriter
import GeoIPApiService
import GeoIPDatabaseService

app = typer.Typer()


@app.command()
def parse(input_file: str,
          output_file: str = "ipList.txt"):
    my_parser: MyParser = MyParser()
    my_writer: MyWriter = MyWriter()
    my_writer.write_ip_list(my_parser.parse_input_file(input_file), output_file)

@app.command()
def locate(input_file: str,
           output_file: str = "geoIPs.txt",
           use_cache: bool = True,
           local_database: bool = True):
    my_parser: MyParser = MyParser()
    my_caching: MyCaching = MyCaching()
    my_writer: MyWriter = MyWriter()
    config = my_parser.parse_config()
    ip_list = my_parser.parse_ip_file(input_file)
    data = {}

    # both GeoIPDatabaseService and GeoIPApiService implement the
    # interface for GeoIPService however I don't know how to add interfaces
    if local_database:
        location_service= GeoIPDatabaseService(config)
    else:
        location_service= GeoIPApiService(config)

    for ip in ip_list:
        try:
            data[ip] = my_caching.put_in_cache(ip, location_service.find_data(ip, use_cache))
        except HTTPError:
            print("ran out of api requests saving work to file and exiting, try using the database option")
            my_writer.write_locate_list(data, output_file)

    my_writer.write_locate_list(data, output_file)

@app.command()
def whos(input_file: str,
         output_file: str = "rdapIPs.txt",
         use_cache: bool = True):
    # TODO

@app.command()
def search(ip: str):
    r = redis.Redis(host='localhost', port=6379, db=0)
    print(r.get(ip))


if __name__ == "__main__":
    app()