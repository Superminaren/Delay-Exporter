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
LOG_LEVEL = 0 # 0 = Debug, 1 = Info, 2 = Warnings, 3 = Critical
CONFIG_LOCATION = "./config.ini" # Config location, defaults

# Arrays of configuration data.
settings = {"APIKey", "Port", "SiteID", "LogLevel", "ReloadTimeMinutes"}
transportMethods = {"Buses","Trains","Trams","Ships"}

# Metrics for prometheus_client library
traffic_delay_time =    Gauge('traffic_delay_seconds','Average traffic delay over next 60 minute period',           ["transportMethod"])
traffic_delay_count = Counter('traffic_delay_count',  'Average traffic delay over next 60 minute period',           ["transportMethod"])
traffic_count =       Counter('traffic_count',        'Amount of given transport method over next 60 minute period',["transportMethod"])


#TODO Change all privates to __variables

# Class instances

__API = APIHandler.APIHandler()
log = Logger.Logger(LOG_LEVEL) # Define log level for levels of verbosity
config = configparser.ConfigParser()  # Defining a config parser for easy config

def get_settings():

    # Changes where to load in config from based off system arguments.

    if len(sys.argv) > 1:                                                       # If argument is supplied, load config from provided location.
        CONFIG_LOCATION=sys.argv[1]
        log.debug(CONFIG_LOCATION+ " loaded.")
    else:
        CONFIG_LOCATION="./config.ini"

    config.sections()
    config.read(CONFIG_LOCATION)
    try:
        for var in settings:
            if var not in config['EXPORTER']:
                log.critical("Missing setting: "+var)
                exit(1)
            else:
                log.info((var + ": " + config['EXPORTER'][var]))
    except KeyError as e:
        log.critical(CONFIG_LOCATION+" not found!")
        exit(1)
    log.info("Configuration successfully imported.")

def run():

    # Start up the server to expose metrics.
    # First set all config

    __API.init(config)                                                           # Sets configuration for APIHandler instance
    start_http_server(int(config['EXPORTER']['Port']))                           # Starts http_server on specified port
    log.info("Initialized Prometheus Exporter.")
    while True:
        update_exporter()                                                        # Fetches data through dataHandler
        time.sleep(int(config['EXPORTER']['ReloadTimeMinutes'])*60)              # Sleep specified time in config after update



def update_exporter():

    # Updates the prometheus exporter values
    # Then stores metrics, specific to each mode of transportation

    __API.update_data()
    for method in transportMethods:
        traffic_delay_time.labels(transportMethod=method).set(__API.get_delay_average(method))
        traffic_delay_count.labels(transportMethod=method).inc(__API.get_delay_count(method))
        traffic_count.labels(transportMethod=method).inc(__API.get_count(method))

if __name__ == '__main__':
    get_settings()
    run()