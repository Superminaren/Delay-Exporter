#!/usr/bin/python3
from prometheus_client import start_http_server, Gauge, Counter
import sys
import time
import APIHandler as APIHandler
import Logger
import configparser


#Config variables

PORT = 8000
UPDATE_TIME_MINUTES = 60 # Recommended to not update more often than 5 minutes due to limited API Calls
LOG_LEVEL = 0 #0 = Debug, 1 = Info, 2 = Warnings, 3 = Critical
LOG_LOCATION = "./config.ini" # Config location, defaults

# Arrays of configuration data.
settings = {"APIKey", "Port", "SiteID", "LogLevel", "ReloadTimeMinutes", "URL"}
transportMethods = {"Buses","Trains","Trams","Ships"}

# Metrics for prometheus_client library
delay_time = Gauge('traffic_delay_seconds','Average traffic delay over next 60 minute period', ["transportMethod"])
delay_count = Counter('traffic_delay_count','Average traffic delay over next 60 minute period', ["transportMethod"])
#TODO Change all privates to __variables

# Class instances
__API = APIHandler.APIHandler()
log = Logger.Logger(LOG_LEVEL) # Define log level for levels of verbosity
config = configparser.ConfigParser()  # Defining a config parser for easy config

def get_settings():

    # Changes where to load in config from based off system arguments.
    if len(sys.argv) > 1: #If argument is supplied
        LOG_LOCATION=sys.argv[1]
        print(LOG_LOCATION)
    else:
        LOG_LOCATION="./config.ini"

    config.sections()
    config.read(LOG_LOCATION)
    try:
        for var in settings:
            if var not in config['EXPORTER']:
                log.critical("Missing setting: "+var)
                exit(0)
            else:
                log.info((var + ": " + config['EXPORTER'][var]))
    except KeyError as e: # If key is missing or file is not found.
        print(LOG_LOCATION," not found!")
        exit(0)


def run():

    # Start up the server to expose metrics.
    __API.init(config)  # Initialize with json config

    start_http_server(int(config['EXPORTER']['Port']))
    log.info("Initialized Prometheus Exporter.")
    while True:
        update_exporter() # Fetches data through dataHandler
        time.sleep(UPDATE_TIME_MINUTES*60) # Sleep specified time in config after update TODO Change value to 3600 for production


# Updates the prometheus exporter values
def update_exporter():
    __API.update_data()
    for method in transportMethods:
        delay_time.labels(transportMethod=method).set(__API.get_average_delay(method))
        delay_count.labels(transportMethod=method).inc(__API.get_delay_count(method))


if __name__ == '__main__':
    get_settings()
    run()