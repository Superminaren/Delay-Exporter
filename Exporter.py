#!/usr/bin/python3
from prometheus_client import start_http_server, Gauge, Counter
import time
import APIHandler as APIHandler
import Logger
import configparser


#Config variables

PORT = 8000
SITEID = 8254 #Location ID From "SL Platsinfo" API.
UPDATE_TIME_MINUTES = 5 # Recommended to not update more often than 5 minutes due to limited API Calls
LOG_LEVEL = 0 #0 = Debug, 1 = Info, 2 = Warnings, 3 = Critical
#LOG_LOCATION = "/etc/prometheus-sl-exporter.conf"
LOG_LOCATION = "/etc/prometheus-sl-exporter.conf"


settings = {"APIKey", "Port", "SiteID", "LogLevel"}
transportMethods = {"Buses","Trains","Trams","Ships"}

#Metric names
delay_time = Gauge('traffic_delay_seconds','Average traffic delay over next 60 minute period', ["transportMethod"])
delay_count = Counter('traffic_delay_count','Average traffic delay over next 60 minute period', ["transportMethod"])

#Class instances
API = APIHandler.APIHandler()
log = Logger.Logger(LOG_LEVEL) #
config = configparser.ConfigParser()  # Defining a config parser for easy config


def run():
    API.init(config['EXPORTER']['APIKey'], SITEID)  # Initialize with config
    # Start up the server to expose metrics.
    start_http_server(PORT)
    log.info("Initialized Prometheus Exporter.")
    while True:
        update_exporter() # Fetches data through dataHandler
        time.sleep(UPDATE_TIME_MINUTES*60) # Sleep for an hour before next update TODO Change value to 3600 for production

def update_exporter():
    API.update(SITEID, UPDATE_TIME_MINUTES)
    for method in transportMethods:
        delay_time.labels(transportMethod=method).set(API.get_average_delay(method))
        delay_count.labels(transportMethod=method).inc(API.get_delay_count(method))

def get_settings():
    config.sections()
    config.read('config.ini')
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


if __name__ == '__main__':
    get_settings()
    run()