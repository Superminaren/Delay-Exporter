# Carl Vargklint 2020-01-18
# This prometheus exporter is for use with the SL Realtidsinformation 4 API.
class APIHandler:
	from datetime import datetime

	import json
	import requests
	import Logger

	data = None
	APIKEY = ""
	PORT = 8000
	SITEID = 8254
	UPDATE_TIME_MINUTES = 60
	TIMEFORMAT = '%Y-%m-%dT%H:%M:%S'

	DELAY_TIME = 60 # Delay time in seconds required for something to be considered delayed.
	templateURL = "https://api.sl.se/api2/realtimedeparturesV4.json?key=<KEY>&siteid=<SITEID>&timewindow=<TIMEWINDOW>"
	#URL = "https://api.sl.se/api2/realtimedeparturesV4.json?key=APIKEY&siteid=SITEID&timewindow=60"
	#URL.replace("APIKEY",APIKEY)

	#URL.replace("SITEID", str(SITEID))
	URL = "https://uwu.party/testresponse.txt"

	#Logging class
	log = Logger.Logger(0)
	#Init function to prevent
	def init(self,apikey, siteid):
		APIKEY = apikey
		self.data = self.__get_json_data(siteid)

	#Run update before getting data
	def update(self, SITE, UPDATE_TIME_MINUTES):
		self.URL = self.templateURL.replace("<KEY>", self.APIKEY).replace("<SITEID>", str(self.SITEID)).replace("<TIMEWINDOW>", str(self.UPDATE_TIME_MINUTES))
		print(self.URL)
		self.log.debug("Updating API Data")
		self.SITEID=SITE
		data = self.__get_json_data(self.SITEID)
		return data



	# Parses string timestamp into datetime format for easy comparison
	def __parse_time(self, t):
		return self.datetime.strptime(t,self.TIMEFORMAT)


	# Makes a HTTP Request and returns json response.
	def __get_json_data(self, siteid):
		self.SITEID = siteid
		resp = self.requests.get(self.URL)
		data = resp.text
		return self.json.loads(data)

	def __verify_json_data(self,data):
		if data['StatusCode'] != 0:
			self.log.critical("Incorrect statuscode or missing data.")
			#print("API Error:", data)
			return "" #No elements in case of error



	# Returns the average of all delays for a specified transport method
	def get_average_delay(self, transport):
		count = 0
		total = 0
		for x in self.data['ResponseData'][transport]:
			#print(x)
			date = self.__parse_time(x['ExpectedDateTime'])-self.__parse_time(x['TimeTabledDateTime'])
			if (date.seconds>0):
				count = count + 1
				total = total + date.seconds
		if count == 0:
			return 0
		else:
			return total/count


	# Returns the amount of delays over the defined limit
	def get_delay_count(self,transport):
		count = 0
		for x in self.data['ResponseData'][transport]:
			date = self.__parse_time(x['ExpectedDateTime']) - self.__parse_time(x['TimeTabledDateTime'])
			if (date.seconds > self.DELAY_TIME):
				count = count + 1
		return count

	# Returns the amount of any transport method per hour.
	def get_count(self, transport):
		count = 0
		for x in self.data['ResponseData'][transport]:
			count = count + 1
		return count