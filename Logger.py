class Logger:
    import time
    LOG_LEVEL = 0
    DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


    def __init__(self, LOG_LEVEL):
        self.LOG_LEVEL = LOG_LEVEL

    #Called to check loglevels, more compact
    def __log(self, logData, level):
        if level>=self.LOG_LEVEL:
            print(self.time.strftime(self.DATE_FORMAT,self.time.gmtime()), ":",logData)

    def set_log_level(self, level):
        self.LOG_LEVEL = level
    #Debug
    def debug(self, logData):
        self.__log("DEBUG: " + logData, 0 )
    # Info
    def info(self, logData):
        self.__log("INFO: " + logData, 1 )
    # Warnings
    def warning(self, logData):
        self.__log("WARN: " + logData, 2 )
    # Critical
    def critical(self, logData):
        self.__log("CRITICAL: " + logData, 3 )

