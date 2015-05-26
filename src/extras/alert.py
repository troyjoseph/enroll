#!/usr/bin/env python
#OSX ONLY b/c of use pf command+t, change for windows
###FEEDBACK, NEW NAME, WHEN SHOULD I START explination, hover change text color 
##DON't CLOSE AFTER ENROL
##ACTIVATION KEY TAKE FROM GOOGLE DOCS SPREADSHEET

#must install phantom.js
import requests, thread, time, os, datetime
from sys import stdout

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class Bot(): 
	def __init__(self):
		self.timeout = 5

	def alert(self, netid, password, className, only = True):
		self.driver = webdriver.PhantomJS('phantomjs')
		url = requests.get('http://studentcenter.cornell.edu', allow_redirects = True).url
		self.driver.get(url)
		self.driver.find_element_by_id('netid').send_keys(netid)
		if (password != ''):
			self.driver.find_element_by_id('password').send_keys(password)
			self.driver.find_element_by_name('Submit').click()
		self.loadingNOTO('Student Center')
		self.driver.find_element_by_id('DERIVED_SSS_SCL_LINK_ADD_ENRL').click()
		self.loading('Select classes to add')

		self.driver.find_element_by_id('DERIVED_REGFRM1_CLASS_NBR$42$').send_keys(className)
		self.driver.find_element_by_id('DERIVED_REGFRM1_SSR_PB_ADDTOLIST2$44$').click()
		self.loading('Section')

		length = self.getLength(only)
		print 'ready'
		print length
		length = 1
		for x in range(0,length):
			thread.start_new_thread(self.section, (x,netid,password,className,))
		time.sleep(99999999)

	def getLength(self, only):
		if (only == True):
			xpath = '//*[@id="SSR_CLS_TBL_RE$scroll$0"]/tbody/tr[1]/td/table/tbody/tr['
			table = 'RE'
		else:
			xpath = '//*[@id="SSR_CLS_TBL_R1$scroll$0"]/tbody/tr[2]/td/table/tbody/tr['
			table = 'R1'
		length = 0
		if (only ==True):
			try:
				length = int(str(self.driver.find_element_by_xpath('//*[@id="SSR_CLS_TBL_RE$scroll$0"]/tbody/tr[2]/td/span[3]').text)[-2:])
				tablelength = int(str(self.driver.find_element_by_xpath('//*[@id="SSR_CLS_TBL_RE$scroll$0"]/tbody/tr[2]/td/span[3]').text)[2:4])
			except:
				try:
					length = int(str(self.driver.find_element_by_xpath('//*[@id="SSR_CLS_TBL_RE$scroll$0"]/tbody/tr[2]/td/span[2]').text)[-2:])
					tablelength = int(str(self.driver.find_element_by_xpath('//*[@id="SSR_CLS_TBL_RE$scroll$0"]/tbody/tr[2]/td/span[2]').text)[2:4])
				except:
					print "Can't find length"
					length = 20
					tablelength = 5

		else:
			try:
				length =  int(str(self.driver.find_element_by_xpath('//*[@id="SSR_CLS_TBL_R1$scroll$0"]/tbody/tr[3]/td/span[2]').text)[-2:])
				tablelength = int(str(self.driver.find_element_by_xpath('//*[@id="SSR_CLS_TBL_R1$scroll$0"]/tbody/tr[3]/td/span[2]').text)[2:4])
			except:
				try:
					length = int(str(self.driver.find_element_by_xpath('//*[@id="SSR_CLS_TBL_R1$scroll$0"]/tbody/tr[3]/td/span[3]').text)[-2:])
					tablelength = int(str(self.driver.find_element_by_xpath('//*[@id="SSR_CLS_TBL_R1$scroll$0"]/tbody/tr[3]/td/span[3]').text)[2:4])

				except:
					print "Can't find length"
					length = 20
					tablelength = 5


		return length

	def section(self, number,netid,password,className):
		print 'start'
		self.driver = webdriver.PhantomJS('phantomjs')
		url = requests.get('http://studentcenter.cornell.edu', allow_redirects = True).url
		self.driver.get(url)
		self.driver.find_element_by_id('netid').send_keys(netid)
		if (password != ''):
			self.driver.find_element_by_id('password').send_keys(password)
			self.driver.find_element_by_name('Submit').click()
		self.loadingNOTO('Student Center')
		self.driver.find_element_by_id('DERIVED_SSS_SCL_LINK_ADD_ENRL').click()
		self.loading('Select classes to add')

		self.driver.find_element_by_id('DERIVED_REGFRM1_CLASS_NBR$42$').send_keys(className)
		self.driver.find_element_by_id('DERIVED_REGFRM1_SSR_PB_ADDTOLIST2$44$').click()
		self.loading('Section')
		try: 

				e = self.driver.find_element_by_xpath( ('//*[@id="R1_SECTION$'+str(number)+'"]') ).click()
			
				capacity = self.driver.find_element_by_xpath('//*[@id="ACE_width"]tr[10]/tbody/tr[5]/td[2]/span').text
				for x in capacity:
					print x
				total = self.driver.find_element_by_xpath('//*[@id="ACE_width"]/tbody/tr[5]/td[2]/span').text
				print capacity
				print total
				#if (seats>0):
				#	print 'Found a seat!'
		except Exception, e:
				print str(e)
				print 'failed!'
				pass
	
	def loadingNOTO(self, text):
		loaded = False
		_time = time.time()
		while(loaded == False):
			src = self.driver.page_source
			if(text in src):
				loaded = True

	def loading(self, text):
		loaded = False
		_time = time.time()
		while(loaded == False):
			src = self.driver.page_source
			if(text in src):
				loaded = True
			if(time.time()-_time>self.timeout):
				print 'TIMEOUT'
				break
	
	def loadingClick(self, text):
		loaded = False
		_time = time.time()
		while(loaded == False):
			try:
				self.driver.find_element_by_id(text).click()
				loaded = True
			except:
				loaded = False
			if(time.time()-_time>self.timeout):
				print 'TIMEOUT'
				break

	#used for page that may or may not appear	
	def loadingClickTO(self, text, text2):
		loaded = False
		_time = time.time()
		while(loaded == False):
			try:
				self.driver.find_element_by_id(text).click()
				loaded = True
			except:
				loaded = False
			src = self.driver.page_source
			if(text2 in src):
				loaded = True
			if(time.time()-_time>self.timeout):
				print 'TIMEOUT'
				break