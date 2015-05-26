#!/usr/bin/env python
#OSX ONLY b/c of use pf command+t, change for windows
###FEEDBACK, NEW NAME, WHEN SHOULD I START explination, hover change text color 
##DON't CLOSE AFTER ENROL
##ACTIVATION KEY TAKE FROM GOOGLE DOCS SPREADSHEET

#must install phantom.js
import requests, thread, time, os, datetime, sys
from sys import stdout

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class Bot(): 
    def __init__(self):
        self.timeout = 180

    def addClass(self, netid, password, hidden = False ):

        if (hidden == False):
            self.driver = webdriver.Firefox()
        else:
            self.driver = webdriver.PhantomJS('phantomjs')
        url = requests.get('http://studentcenter.cornell.edu', allow_redirects = True).url
        self.driver.get(url)
        self.driver.find_element_by_id('netid').send_keys(netid)
        if (password != ''):
            self.driver.find_element_by_id('password').send_keys(password)
            self.driver.find_element_by_name('Submit').click()
        self.loadingNOTO('Student Center')
        print 'Logged in!'
        self.driver.find_element_by_id('DERIVED_SSS_SCL_LINK_ADD_ENRL').click()

        # SELECT SEMESTER
        xpath = '//*[@id="SSR_DUMMY_RECV1$scroll$0"]/tbody/tr[5]/td[1]/input'
        self.driver.find_element_by_xpath(xpath).click()
        self.driver.find_element_by_id('DERIVED_SSS_SCT_SSR_PB_GO').click()

        self.loading('Select classes to add')
        self.add('11509','13301' )
        #   self.add('17985')
        print 'Added classes!'
        print 'Running!'
        while True:
            self.repeat()

        time.sleep(3)
        self.driver.close()

    def add(self, classname, discussion):
        self.driver.find_element_by_id('DERIVED_REGFRM1_CLASS_NBR$42$').send_keys(classname)
        self.driver.find_element_by_id('DERIVED_REGFRM1_SSR_PB_ADDTOLIST2$44$').click()
        self.loading('Section')

        # ADD DISCUSSION
        print 'add discussion'
        xpath = '//*[@id="SSR_CLS_TBL_RE$scroll$0"]/tbody/tr[1]/td/table/tbody/tr['
        # //*[@id="SSR_CLS_TBL_RE$scroll$0"]/tbody/tr[1]/td/table/tbody/tr[10]/td[1]/input
        table = 'RE'
        tablelength = 11
        length = 11

        _found = False
        for i in range(2,tablelength+2):
            try: 
                e = self.driver.find_element_by_xpath( (xpath+str(i)+']/td[2]/span') ).text
                print(e)
                if (str(e)==str(discussion)):
                    _found = True
                    self.driver.find_element_by_xpath(xpath+str(i)+']/td[1]/input').click()
                    break
            except:
                print
        x = 5
        while(x<length and _found == False):    
            self.driver.find_element_by_name('SSR_CLS_TBL_'+table+'$fdown$img$0').click()
            #self.loadingSection(x+5)
            for i in range(2,tablelength+2):
                try: 
                    e = self.driver.find_element_by_xpath( (xpath+str(i)+']/td[2]/span') ).text
                    print str(e)
                    if (str(e)==str(discussion)):
                        _found = True
                        self.driver.find_element_by_xpath(xpath+str(i)+']/td[1]/input').click()
                        break
                except:
                    print
            x+=5

        self.loadingClick('DERIVED_CLS_DTL_NEXT_PB')
        self.loadingClickTO('DERIVED_CLS_DTL_NEXT_PB', 'has been added to your')
        self.loadingClickTO('DERIVED_CLS_DTL_NEXT_PB','has been added to your')
        self.loadingClickTO('DERIVED_CLS_DTL_NEXT_PB','has been added to your')    
        self.repeat()

    def repeat(self):
        self.loadingClick('DERIVED_REGFRM1_LINK_ADD_ENRL')
        self.loading('Click Finish Enrolling to process your request')
        self.loadingClick('DERIVED_REGFRM1_SSR_PB_SUBMIT')
        self.loadingClick('DERIVED_REGFRM1_SSR_PB_FIX_ERRORS')

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

    def is_integer(self, s):
        try:
            int(s)
            return True
        except ValueError:
            return False
    


if __name__ == "__main__":
    b = Bot()
    try: 
        netid = sys.argv[1]
        password = sys.argv[2]
        b.addClass(str(netid),str(password), hidden = True)
    except:
        b.addClass("","")