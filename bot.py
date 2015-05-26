#!/usr/bin/env python
import requests, thread, os

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

netid ='tcj29'
password='tc2013j@cony'
url = requests.get('http://studentcenter.cornell.edu', allow_redirects = True).url

chromedriver = "/Users/troy/Downloads/chromedriver"
os.environ["webdriver.chrome.driver"] = chromedriver
driver = webdriver.Chrome(chromedriver)

def addClass(className, cookies):
	print className
	_driver = webdriver.Chrome(chromedriver)
	_driver.add_cookies(cookies)
	_driver.get(baseurl)


driver = webdriver.Chrome(chromedriver)

try:
	driver.get(url)
	driver.find_element_by_id('netid').send_keys(netid)
	driver.find_element_by_id('password').send_keys(password)
	driver.find_element_by_name('Submit').click()
	driver.find_element_by_id('DERIVED_SSS_SCL_LINK_ADD_ENRL').click()

	baseurl = driver.current_url
	cookies = driver.get_cookies()

	thread.start_new_thread( addClass, ("name", ) )

except Exception,e: print str(e)

while(True):
	continue 

#finally:
#	driver.close()



	