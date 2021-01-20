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
	__URL = "NEEDSTOCHANGE"


	#Logging class
	log = Logger.Logger(0)

	# Init function to prevent NoneTypes

	def init(self, config):
		self.templateURL = config['EXPORTER']['URL']
		self.APIKEY = config['EXPORTER']['APIKey']
		self.SITEID = config['EXPORTER']['SiteID']
		self.UPDATE_TIME_MINUTES = int(config['EXPORTER']['ReloadTimeMinutes'])
		self.update_url()
		self.update_data()


	#Run update before getting data
	def update_data(self):

		self.log.debug("Updating API Data"+"\n URL: "+self.__URL)
		self.data = self.__get_json_data()
		return self.data

	def update_url(self):
		self.__URL = self.templateURL\
			.replace("<KEY>", str(self.APIKEY))\
			.replace("<SITEID>", str(self.SITEID))\
			.replace("<TIMEWINDOW>", str(self.UPDATE_TIME_MINUTES))\
			.replace("\"","")
		return self.__URL

	# Parses string timestamp into datetime format for easy comparison
	def __parse_time(self, t):
		return self.datetime.strptime(t,self.TIME_FORMAT)


	# Makes a HTTP Request and returns json response.
	def __get_json_data(self):
		print("Get Json Data : ", self.__URL)
		try:
			resp = self.requests.get(self.__URL)
			data = resp.text
			return self.json.loads(data)
		except Exception as e:
			print(e); exit(0)


	def __verify_json_data(self,data):
		if data['StatusCode'] != 0:
			self.log.critical("Incorrect statuscode or missing data.")
			#print("API Error:", data)
			return "" #No elements in case of error



	# Returns the average of all delays for a specified transport method
	def get_average_delay(self, transport):
		count = 0
		total = 0
		print(self.data)
		for x in self.data['ResponseData'][transport]:
			#print(x)
			date = self.__parse_time(x['ExpectedDateTime'])-self.__parse_time(x['TimeTabledDateTime'])
			if (date.seconds>0):
				count = count + 1
				total = total + date.seconds

		if count == 0:
			return 0
		else:
			self.log.debug("Average_Delay for "+transport+" is: "+str((total / count)))
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
		return count

