import typer

app = typer.Typer()


@app.command()
def parse(inputFile: str,
          outputFile: str = "ipList.txt"):
    writeIPList(parseInputFile(inputFile), outputFile)

@app.command()
def locate(inputFile: str,
           outputFile: str = "geoIPs.txt",
           useCache: bool = True,
           localDatabase: bool = True):

    ipList = parseIPFile(inputFile)

    if localDatabase:
        locationService: GeoIP2DatabaseService = new GeoIPDatabaseService()
    else:
        locationService: GeoIP2DatabaseService = new GeoIPApiService

    if useCache:
        for ip in ipList:


    if useCache:
        if localDatabase:
            grabGeoIpData(getListOfIPs(inputFile))
    # TODO locate

@app.command()
def whos(inputFile: str,
         outputFile: str = "rdapIPs.txt",
         useCache: bool = True):
    # TODO

def search(ip: str):
    # TODO
