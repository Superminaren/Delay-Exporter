"""This prometheus exporter is for use with the SL Realtidsinformation 4 API."""
__author__      = "Carl Vargklint"

class APIHandler:
	from datetime import datetime
	import json
	import requests
	import Logger


	data = None
	APIKEY = ""
	SITEID = 8254
	UPDATE_TIME_MINUTES = 60
	TIME_FORMAT = '%Y-%m-%dT%H:%M:%S'
	DELAY_TIME = 60 # Delay time in seconds required for something to be considered delayed.



	templateURL = "https://api.sl.se/api2/realtimedeparturesV4.json?key=<KEY>&siteid=<SITEID>&timewindow=<TIMEWINDOW>"
	__URL = ""


	#Logging class
	log = Logger.Logger(0)

	# Init function
	# Reason for no __init__?
	# This allows me to initialize the instance whenever after being declared.

	def init(self, config):
		#Check for dynamic variables in config file
		if 'URL' in config['EXPORTER']:
			self.templateURL = config['EXPORTER']['URL']

		# Copy static variables from config file
		self.APIKEY = config['EXPORTER']['APIKey']
		self.SITEID = config['EXPORTER']['SiteID']
		self.UPDATE_TIME_MINUTES = int(config['EXPORTER']['ReloadTimeMinutes'])
		#Switch log level
		self.log.set_log_level(int(config['EXPORTER']['LogLevel']))

		# Insert parameters for API URL
		self.__URL = self.templateURL\
			.replace("<KEY>", str(self.APIKEY))\
			.replace("<SITEID>", str(self.SITEID))\
			.replace("<TIMEWINDOW>", str(self.UPDATE_TIME_MINUTES))\
			.replace("\"","")
		self.update_data()


	# Runs update and fetches data
	def update_data(self):
		self.log.debug("Updating API Data"+"\n URL: "+self.__URL)
		self.data = self.__get_json_data()
		return self.data

	# Parses string timestamp into datetime format for easy comparison
	def __parse_time(self, t):
		return self.datetime.strptime(t,self.TIME_FORMAT)


	# Makes a HTTP Request and returns json response.
	def __get_json_data(self):
		self.log.debug("Getting JSON data for URL: "+self.__URL)
		try:
			resp = self.requests.get(self.__URL)
			self.data = resp.text
			return resp.json()
		except Exception as e:
			print(e)
			exit(1)

	# Verify data integrity
	# TODO Improve checking

	def __verify_json_data(self,data):
		if len(data)<1:
			self.log.critical("Incorrect data size. Is ")
			return False
		if data['StatusCode'] != 0:
			self.log.critical("Incorrect statuscode or missing data.")
			return False
		return True



	# Returns the average of all delays for a specified transport method

	def get_delay_average(self, transport):
		count = 0
		total = 0
		for x in self.data['ResponseData'][transport]:
			date = self.__parse_time(x['ExpectedDateTime'])-self.__parse_time(x['TimeTabledDateTime'])
			if (date.seconds>0):
				count = count + 1
				total = total + date.seconds
		#a = lambda x: 0 if (x == 0) else (total / x)
		#return a(count)
		if count == 0:
			return 0
		else:
			self.log.debug("Average_Delay for " + transport + " is: " + str((total / count)))
			return total/count

	# Returns the amount of delays over the defined limit
	def get_delay_count(self,transport):
		count = 0
		for x in self.data['ResponseData'][transport]:
			date = self.__parse_time(x['ExpectedDateTime']) - self.__parse_time(x['TimeTabledDateTime'])
			if (date.seconds > self.DELAY_TIME):
				count = count + 1
		self.log.debug("Delays for "+transport+" are: "+str(count))
		return count

	# Returns the amount of any transport method per hour.
	def get_count(self, transport):
		count = 0
		for x in self.data['ResponseData'][transport]:
			count = count + 1
		self.log.debug("Amount of "+transport+" for next 60 minutes are: "+str(count))
		return count

