#!/usr/bin/env python
#OSX ONLY b/c of use pf command+t, change for windows

from splinter import Browser
import requests, thread, time, os

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

netid ='tcj29'
password='tc2013j@cony'

chromedriver = "/Users/troy/Downloads/chromedriver"
os.environ["webdriver.chrome.driver"] = chromedriver


def addClass(className):
	print className
	url = requests.get('http://studentcenter.cornell.edu', allow_redirects = True).url
	_driver = webdriver.Firefox()
	_start = time.time()
	_driver.get(url)
	_driver.find_element_by_id('netid').send_keys(netid)
	_driver.find_element_by_id('password').send_keys(password)
	_driver.find_element_by_name('Submit').click()

	_driver.find_element_by_id('DERIVED_SSS_SCL_LINK_ADD_ENRL').click()

	print time.time()-_start
	time.sleep(1)
	_driver.close() 

thread.start_new_thread( addClass, ("name", ) )
thread.start_new_thread( addClass, ("name2", ) )

url = requests.get('http://studentcenter.cornell.edu', allow_redirects = True).url
driver = webdriver.Firefox()
start = time.time()
driver.get(url)
driver.find_element_by_id('netid').send_keys(netid)
driver.find_element_by_id('password').send_keys(password)
driver.find_element_by_name('Submit').click()

driver.find_element_by_id('DERIVED_SSS_SCL_LINK_ADD_ENRL').click()

print time.time()-start
time.sleep(5)
driver.close() 
