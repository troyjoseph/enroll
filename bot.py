#!/usr/bin/env python
#OSX ONLY b/c of use pf command+t, change for windows

from splinter import Browser
import requests, thread

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

netid ='tcj29'
password='tc2013j@cony'
url = requests.get('http://studentcenter.cornell.edu', allow_redirects = True).url

driver = webdriver.Firefox()
try:
	driver.get(url)
	driver.find_element_by_id('netid').send_keys(netid)
	driver.find_element_by_id('password').send_keys(password)
	driver.find_element_by_name('Submit').click()

	baseurl = driver.current_url
	thread.start_new_thread( addClass, ("name", ) )

except Exception,e: print str(e)

#finally:
#	driver.close()


def addClass(className):
	print className
	_driver = webdriver.Firefox()
	_driver.get(baseurl)
	body = _driver.find_element_by_tag_name("body")
	
	