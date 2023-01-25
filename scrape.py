import requests
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime
import time

#!pip install webdriver-manager

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import chrome_driver_autoinstaller

import requests
import json

from pyvirtualdisplay import Display
display = Display(visibla=0, size=(800, 800))
display.start()

chrome_driver_autoinstaller.install()

chrome_options = webdriver.ChromeOptions()
options = [
	'--window-size=1200,1200',
	'--ignore-certificate-errors'

		#"--headless",
    #"--disable-gpu",
    #"--window-size=1920,1200",
    #"--ignore-certificate-errors",
    #"--disable-extensions",
    #"--no-sandbox",
    #"--disable-dev-shm-usage",
    #'--remote-debugging-port=9222'
]

for option in options:
	chrome_options.add_argument(option)

driver = webdriver.Chrome(options=chrome_options)


ggeocode = 'AIzaSyACn8ZsmhM9DjpK6MYUApfscEnQypC6LjY'

# location from google
def get_location_coordinates(location):
	geo_url = f'https://maps.googleapis.com/maps/api/geocode/json?address={location}&key={ggeocode}'
	response = requests.get(geo_url)
	content = response.content.decode('utf8')
	geo_js = json.loads(content)
	geo_status = geo_js['status']

	if geo_status == 'OK':
		geo_elements = geo_js['results'][0]
		geometry = geo_elements['geometry']
		location_coordinates = geometry['location']
		location_lat = location_coordinates['lat']
		location_long = location_coordinates['lng']
		return (location_lat, location_long)
	else:
		return (None, None)

def scrape_weather(jsonify=False):
	driver.get('https://severeweather.wmo.int/v2/list.html')
	try:
		elem = WebDriverWait(driver, 30).util(
	EC.presence_of_element_located((By.CLASS_NAME, 'dataTables_scrollBody'))
	)
	finally:
		print('loaded')
		soup = BeautifulSoup(driver.page_source, 'html.parser')
	all = soup.findAll('tbody')[2]
	row = all.findAll('tr')
	rest_info = []

	for i in row:
		infos_row = i.findAll('td')
		for index, j in enumerate(infos_row):
			info = None
			if index == 0:
				info = j.find('span')
				event = info.text

			if index == 4:
				info = j.find('span')
				areas = info.text

			if index == 1:
				issued_time = j.text

			if index == 3:
				country = j.text

			if index == 5:
				regions = j.text

			if index == 2:
				continue

		rest_info.append([event, issued_time, country, areas, regions, datetime.today().strftime('%Y-%m-%d %H:%M')])

	df = pd.DataFrame(rest_info, columns=['Event_type', 'Issued_time', 'Country', 'Areas', 'Regions', 'Date'])
	df['Issued_time'] = df['Issued_time'].apply(lambda x: x.split('#')[0]) 
	df['coordinates'] = df['Areas'] + ', ' + df['Country']
	df['geo_location'] = df['coordinates'].apply(get_location_coordinates)

	if jsonify:
		result = df.to_json(orient='split')
		parsed = json.loads(result)
		return json.dumps(parsed)
	else:
		df.to_csv('scraped_weather.csv', mode='a', index=False, header=False)


def scrape_pirates(jsonify=False):
	URL = 'https://www.icc-ccs.org/index.php/piracy-reporting-centre/live-piracy-report'
	rest_info = []
	r = requests.get(URL)
	soup = BeautifulSoup(r.content, 'html.parser')
	all = soup[.find('tbody')
	row = all.findAll('tr')
	for i in row:
		infos_row = i.findAll('td')
		for index, j in enumerate(infos_row):
			if index == 0:
				attack_number =  j.text.replace('\n','').replace('\t','').replace('\r','')
			if index == 1:
				narrations = j.text.replace('\n','').replace('\t','').replace('\r','')
			if index ==2:
				date_of_incident = j.text.replace('\n','').replace('\t','').replace('\r','')
			if index >2:
					continue
		try: 
			rest_info.append([attack_number,narrations,date_of_incident,datetime.today().strftime('%Y-%m-%d %H:%M')])
		except:
			continue

	df_pirates = pd.DataFrame(rest_info, columns = ['attack_nr', 'text', 'date_of_incident', 'scrape_date'])
	df_pirates['text'] = df_pirates['text'].apply(lambda x: x.split('Posn: ')[1])
	df_pirates['location'] = df_pirates['location'].apply(get_location_coordinates)
	df_pirates['geo_location'] = df_pirates['location'].apply(get_location_coordinates)

	if jsonify:
		result = df_pirates.to_json(orient='split')
		parsed = json.loads(result)
		return json.dumps(parsed)
	else:
		df_pirates.to_csv('scraped_pirates.csv', mode='a',  index=False, header=False)

scrape_weather()
scrape_pirates()