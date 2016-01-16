"""

Lamine Ka

This script will send me the local weather via sms every 24 hours

"""

import time
from twilio.rest import TwilioRestClient
import requests
from bs4 import BeautifulSoup as bs

class weather_sms:

	def __init__(self):

		self.send_sms()


	def get_weather(self):
		url = "http://www.wunderground.com/q/zmw:00000.1.61641"

		req = requests.get(url)

		cont = req.content

		html = bs(cont, "html.parser")

		location = html.find("h1", attrs={"class": "city-nav-header"})
		location = str(location.get_text()).strip()

		sun_info = html.find("div", attrs={"class": "sun"}).get_text()

		moon_visivlity = html.find("span", attrs={"class": "nobr"}).get_text()

		wind = str(html.find("span", attrs={"data-variable": "wind_gust_speed"}).get_text()).splitlines()
		wind = str(wind[2])+" "+str(wind[3])

		temp = str(html.find("span", attrs={"data-variable": "heatindex"}).get_text()).strip().splitlines()
		temperature = str(temp[0])+" "+str(temp[1])
		
		self.data = "[LAMINE METEO SERVICE]\n"+location+"\nTemperature: "+temperature+"\nSoleil: "+sun_info+"\nLune: "+moon_visivlity+"\nVent: "+wind

		return self.data



	def send_sms(self):
		
		dests = ["+221779501003", "+221771287650", "+221764823369"]
		msg = self.get_weather()
		accountSID = 'AC863e8e4717ba32e44261c2f9c466e7d0'
		authToken = '1a61389d318d0e924d9856677b795c02'
		my_twilio_num = '+13122199195'
		twilioCli = TwilioRestClient(accountSID, authToken)

		for dest in dests:
			time.sleep(5)
			twilioCli.messages.create(body=msg, from_=my_twilio_num, to=dest)

		print("Sent")



while True:
	weather_sms()
	time.sleep(43200) # every 12 hours
