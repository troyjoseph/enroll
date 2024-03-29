#!/usr/bin/env python
#OSX ONLY b/c of use pf command+t, change for windows
###FEEDBACK, NEW NAME, WHEN SHOULD I START explination, hover change text color 

#must install phantom.js
import requests, thread, time, os, datetime
from sys import stdout

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class Bot(): 
	def __init__(self):
		self.timeout = 5


	def addClass(self, netid, password, className, discussion = None, lab = None, year = 1, test = False ):
		#self.driver = webdriver.Firefox()
		self.driver = webdriver.PhantomJS('phantomjs')
		url = requests.get('http://studentcenter.cornell.edu', allow_redirects = True).url
		self.driver.get(url)
		self.driver.find_element_by_id('netid').send_keys(netid)
		if (password != ''):
			self.driver.find_element_by_id('password').send_keys(password)
			self.driver.find_element_by_name('Submit').click()
		self.loadingNOTO('Student Center')
		self.driver.find_element_by_id('DERIVED_SSS_SCL_LINK_ADD_ENRL').click()
		#self.waitForEnrollmentWindow(year)
		_start = time.time()
		self.loading('Select classes to add')
		self.driver.find_element_by_id('DERIVED_REGFRM1_CLASS_NBR$42$').send_keys(className)
		self.driver.save_screenshot('out1.png')

		self.driver.find_element_by_id('DERIVED_REGFRM1_SSR_PB_ADDTOLIST2$44$').click()
		self.loading('Section')
		if (discussion != None and self.is_integer(discussion)):
				if (lab != None and self.is_integer(lab) ):
					self.addDiscussion(discussion, only = False)
					self.addLab(lab, only = False)
				else:
					self.addDiscussion(discussion, only = True)	
		elif (lab != None and self.is_integer(lab) ):
			self.addLab(lab, only = True)
		self.loadingClick('DERIVED_CLS_DTL_NEXT_PB')
		self.loadingClickTO('DERIVED_CLS_DTL_NEXT_PB', 'has been added to your')
		self.loadingClickTO('DERIVED_CLS_DTL_NEXT_PB','has been added to your')
		self.loadingClickTO('DERIVED_CLS_DTL_NEXT_PB','has been added to your')		
		self.loadingClick('DERIVED_REGFRM1_LINK_ADD_ENRL')
		self.loading('Click Finish Enrolling to process your request')
		#self.loadingClick('DERIVED_REGFRM1_SSR_PB_SUBMIT')
		print time.time()-_start
		if (test == True):
			time.sleep(1)
		else:
			time.sleep(10)
		self.driver.close() 

	def handleLink(self, className):
		print 'handle link'
	
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

	def addDiscussion(self, discussion, only):
		if (only == True):
			xpath = '//*[@id="SSR_CLS_TBL_RE$scroll$0"]/tbody/tr[1]/td/table/tbody/tr['
			table = 'RE'
		else:
			xpath = '//*[@id="SSR_CLS_TBL_R1$scroll$0"]/tbody/tr[2]/td/table/tbody/tr['
			table = 'R1'

		if (only ==True):
			try:
				length = int(str(self.driver.find_element_by_xpath('//*[@id="SSR_CLS_TBL_RE$scroll$0"]/tbody/tr[2]/td/span[3]').text)[-2:])
				tablelength = int(str(self.driver.find_element_by_xpath('//*[@id="SSR_CLS_TBL_RE$scroll$0"]/tbody/tr[2]/td/span[3]').text)[2:3])
			except:
				try:
					length = int(str(self.driver.find_element_by_xpath('//*[@id="SSR_CLS_TBL_RE$scroll$0"]/tbody/tr[2]/td/span[2]').text)[-2:])
					tablelength = int(str(self.driver.find_element_by_xpath('//*[@id="SSR_CLS_TBL_RE$scroll$0"]/tbody/tr[2]/td/span[2]').text)[2:3])
				except:
					print "Can't find length"
					length = 20
					tablelength = 5


		else:
			try:
				length =  int(str(self.driver.find_element_by_xpath('//*[@id="SSR_CLS_TBL_R1$scroll$0"]/tbody/tr[3]/td/span[2]').text)[-2:])
				tablelength = int(str(self.driver.find_element_by_xpath('//*[@id="SSR_CLS_TBL_R1$scroll$0"]/tbody/tr[3]/td/span[2]').text)[2:3])
			except:
				try:
					length = int(str(self.driver.find_element_by_xpath('//*[@id="SSR_CLS_TBL_R1$scroll$0"]/tbody/tr[3]/td/span[3]').text)[-2:])
					tablelength = int(str(self.driver.find_element_by_xpath('//*[@id="SSR_CLS_TBL_R1$scroll$0"]/tbody/tr[3]/td/span[3]').text)[2:3])

				except:
					print "Can't find length"
					length = 20
					tablelength = 5

			


		_found = False
		for i in range(2,tablelength+2):
			try: 
				e = self.driver.find_element_by_xpath( (xpath+str(i)+']/td[2]/span') ).text
				if (str(e)==str(discussion)):
					_found = True
					self.driver.find_element_by_xpath(xpath+str(i)+']/td[1]/input').click()
					break
			except:
				pass
		x = 5
		while(x<length and _found == False):	
			self.driver.find_element_by_name('SSR_CLS_TBL_'+table+'$fdown$img$0').click()
			#self.loadingSection(x+5)
			for i in range(2,tablelength+2):
				try: 
					e = self.driver.find_element_by_xpath( (xpath+str(i)+']/td[2]/span') ).text
					if (str(e)==str(discussion)):
						_found = True
						self.driver.find_element_by_xpath(xpath+str(i)+']/td[1]/input').click()
						break
				except:
					pass
			x+=5
	
	def addLab(self, lab, only):
		if (only == True):
			xpath = '//*[@id="SSR_CLS_TBL_RE$scroll$0"]/tbody/tr[1]/td/table/tbody/tr['
			table = 'RE'
		else:
			xpath = '//*[@id="SSR_CLS_TBL_R2$scroll$0"]/tbody/tr[2]/td/table/tbody/tr['

			table = 'R2'

		if (only ==True):
			try:
				length = int(str(self.driver.find_element_by_xpath('//*[@id="SSR_CLS_TBL_RE$scroll$0"]/tbody/tr[2]/td/span[3]').text)[-2:])
				tablelength = int(str(self.driver.find_element_by_xpath('//*[@id="SSR_CLS_TBL_RE$scroll$0"]/tbody/tr[2]/td/span[3]').text)[2:3])
			except:
				print "Can't find length"
				length = 20
				tablelength = 5
		else:
			try:
				length = int(str(self.driver.find_element_by_xpath('//*[@id="SSR_CLS_TBL_R2$scroll$0"]/tbody/tr[3]/td/span[2]').text)[-2:])
				tablelength = int(str(self.driver.find_element_by_xpath('//*[@id="SSR_CLS_TBL_R2$scroll$0"]/tbody/tr[3]/td/span[2]').text)[2:3])
			except:
				print "Can't find length"
				length = 20
				tablelength = 5


		_found = False
		for i in range(2,tablelength+2):
			try: 
				
				e = self.driver.find_element_by_xpath(xpath+str(i)+']/td[2]/span').text
				if (str(e)==str(lab)):
					_found = True
					self.driver.find_element_by_xpath(xpath+str(i)+']/td[1]/input').click()
					break
			except Exception, e:
				pass 
		x = 5
		while(x<length and _found == False):	
			self.driver.find_element_by_name('SSR_CLS_TBL_'+table+'$fdown$img$0').click()
			#self.loadingSection(x+5)
			for i in range(2,tablelength+2):
				try: 
					e = self.driver.find_element_by_xpath( (xpath+str(i)+']/td[2]/span') ).text
					if (str(e)==str(lab)):
						_found = True
						self.driver.find_element_by_xpath(xpath+str(i)+']/td[1]/input').click()
						break
				except Exception, e:
					pass 
			x+=5
	
	def is_integer(self, s):
	    try:
	        int(s)
	        return True
	    except ValueError:
	        return False
	def waitForEnrollmentWindow(self, year):
			if(int(year) == 1 ): #freshman
				startDate = datetime.datetime.strptime("1/17/15/15/4/00", "%m/%d/%y/%H/%M/%S")
			if(int(year) == 2 ): #sophmore
				startDate = datetime.datetime.strptime("1/17/16/07/00/00", "%m/%d/%y/%H/%M/%S")
			if(int(year) == 3 ): #junior
				startDate = datetime.datetime.strptime("1/17/16/07/00/00", "%m/%d/%y/%H/%M/%S")
			if(int(year) == 4 ): #senior
				startDate = datetime.datetime.strptime("1/17/16/07/00/00", "%m/%d/%y/%H/%M/%S")
			if (startDate > datetime.datetime.now()):
				waiting = True
				while(waiting):
						if (startDate < datetime.datetime.now()):
							waiting = False
							self.driver.execute_script("location.reload()")
							loaded = False
							_time = time.time()
							while(loaded == False):
								src = self.driver.page_source
								if("Select classes to add" in src):
									loaded = True
									print 'no need to hard refresh'
								if(time.time()-_time>1):
									loaded = True
									self.driver.refresh()
											

						t = startDate - datetime.datetime.now()
						stdout.write("\r"+str(t))
						stdout.flush()
						stdout.write("\n")


