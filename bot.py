#!/usr/bin/env python
#OSX ONLY b/c of use pf command+t, change for windows

from splinter import Browser
import requests, thread, time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

netid ='tcj29'
password='tc2013j@cony'

def addClass(className):
	print className
	url = requests.get('http://studentcenter.cornell.edu', allow_redirects = True).url
	_browser = Browser()	
	_start = time.time()
	_browser.visit(url)
	_browser.find_by_id('netid').fill(netid)
	_browser.find_by_id('password').fill(password)
	_browser.find_by_name('Submit').click()

	_browser.find_by_id('DERIVED_SSS_SCL_LINK_ADD_ENRL').click()
	print(time.time()-_start)
	time.sleep(1)
	_browser.quit()

name = 'hello'


thread.start_new_thread( addClass, ("name", ) )
thread.start_new_thread( addClass, ("name2", ) )

url = requests.get('http://studentcenter.cornell.edu', allow_redirects = True).url
browser = Browser()
start = time.time()
browser.visit(url)
browser.find_by_id('netid').fill(netid)
browser.find_by_id('password').fill(password)
browser.find_by_name('Submit').click()

browser.find_by_id('DERIVED_SSS_SCL_LINK_ADD_ENRL').click()
print(time.time()-start)
time.sleep(3)
browser.quit()

