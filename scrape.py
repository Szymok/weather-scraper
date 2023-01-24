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