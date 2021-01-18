
from prometheus_client import start_http_server, Gauge, Counter
import time
import APIHandler as APIHandler
import Logger
import configparser


#Config variables
APIKEY = ""
PORT = 8000
SITEID = 8254 #Location ID From "SL Platsinfo" API.
LOG_LEVEL = 0 #0 = Debug, 1 = Info, 2 = Warnings, 3 = Critical


settings = {"APIKey", "Port", "SiteID", "LogLevel"}
transportMethods = {"Buses","Trains","Trams","Ships"}



#Metric names
delay_time = Gauge('traffic_delay_seconds','Average traffic delay over next 60 minute period', ["transportMethod"])
delay_count = Counter('traffic_delay_count','Average traffic delay over next 60 minute period', ["transportMethod"])

#Class instances
API = APIHandler.APIHandler()
log = Logger.Logger(LOG_LEVEL) #


#if __name__ == '__main__':
def run():
    API.init(APIKEY, SITEID)  # Initialize with config
    # Start up the server to expose metrics.
    start_http_server(PORT)
    log.info("Initialized Prometheus Exporter.")
    while True:
        update_exporter() # Fetches data through dataHandler
        time.sleep(3600) # Sleep for an hour before next update TODO Change value to 3600 for production

def update_exporter():
    API.update(SITEID)
    for method in transportMethods:
        delay_time.labels(transportMethod=method).set(API.get_average_delay(method))
        delay_count.labels(transportMethod=method).inc(API.get_delay_count(method))

def update_settings():
    config = configparser.ConfigParser()  # Defining a config parser for easy config
    config.sections()
    config.read('config.ini')
    for var in settings:
        if var not in config['EXPORTER']:
            log.critical("Missing setting: ", var)
            exit(0)
        else:
            log.info((var + ": " + config['EXPORTER'][var]))

update_settings()
run()