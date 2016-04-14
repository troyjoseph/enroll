#!/usr/bin/env python
import sys
from sys import stdout
import time
import datetime

import warnings
import getpass
import logging
import urllib2

from preferences import Preferences

from selenium import webdriver
from wait import wait_for_page_load


class Bot():

    def __init__(self):
        self.timeout = Preferences.botTimeout
        LOG_FILENAME = 'bot_logfile.log'
        logging.basicConfig(filename=LOG_FILENAME,
                            level=logging.WARNING,)
        logging.captureWarnings(True)
        self._screentShotCount = 0

    def is_integer(self, s):
        try:
            int(s)
            return True
        except ValueError:
            return False

    def addClass(self, netid, password, className, discussion=None, lab=None, test=False, repeat=False):
        self.repeat = repeat
        self._testMode = test
        self.className = className
        self.netid = netid
        self.password = password
        logging.warning('BOT @' + str(self.className) + ': Bot initailized')
        # define settings from preference file #
        self.getPreferences(password)

        self.url = 'http://studentcenter.cornell.edu/'
        #self.url = urllib2.urlopen(self.url).geturl()

        # LOG INTO STUDENT CENTER
        self.goHome()

        # SELECT SEMESTER
        self.selectSemester()

        # WAIT FOR APPOINTMENT
        #self.waitForEnrollmentWindow(self.year)

        self._start = time.time()

        # ENTER CLASS NBR
        '''self.enterClassNbr()

        # Handle adding disscusion and/or lab
        if (discussion is not None and self.is_integer(discussion)):
            if (lab is not None and self.is_integer(lab)):
                logging.warning(
                    'BOT @' + str(self.className) + ': Trying to add discussion and lab')
                self.addDiscussion(discussion, only=False)
                self.addLab(lab, only=False)
            else:
                logging.warning(
                    'BOT @' + str(self.className) + ': Trying to add discussion')
                self.addDiscussion(discussion, only=True)
        elif (lab is not None and self.is_integer(lab)):
            logging.warning(
                'BOT @' + str(self.className) + ': Trying to add lab')
            self.addLab(lab, only=True)

        # Click next until we get back to the home page
        self.clickNextToHome()'''

        # PROCEED to Complete Enrollment
        self.completeEnrollment()

        if (self._testMode):
            time.sleep(1)
        else:
            time.sleep(10)

        self.driver.close()

    def getPreferences(self, password):
        # define settings from preference file, needs password to determine
        # browser type must use firefox is no password is given
        if (int(Preferences.webdriver) == 0 or password == ''):
            self.driver = webdriver.Firefox()
        elif (int(Preferences.webdriver) == 1):
            self.driver = webdriver.PhantomJS()
        else:
            warnings.warn(
                'Invalid webdriver preferences. Using firefox by default')
            self.driver = webdriver.Firefox()
        if (int(Preferences.gradeLevel) == 1 or int(Preferences.gradeLevel) == 2 or
                int(Preferences.gradeLevel) == 3 or int(Preferences.gradeLevel) == 4):
            # 1 = freshman, 2 = sophomore, 3 = junior, 4 = senior
            self.year = Preferences.gradeLevel
        else:
            warnings.warn(
                'Invalid Grade Level preferences. Using freshman by default')
            self.year = 1

    def goHome(self):
        # Got to student center
        with wait_for_page_load(self.driver):
            self.driver.get(self.url)
        src = self.driver.page_source
        
        # if necessary, log in.
        if('CUWebLogin' in src):
            self.driver.find_element_by_id('netid').send_keys(self.netid)
            if (self.password != ''):
                self.driver.find_element_by_id('password').send_keys(self.password)
                with wait_for_page_load(self.driver):
                    self.driver.find_element_by_name('Submit').click()
            logging.warning(
                'BOT @' + str(self.className) + ': Logged into Student Center')

        # Click the 'enroll' button on the main page
        with wait_for_page_load(self.driver):
            self.driver.find_element_by_id(
                'DERIVED_SSS_SCR_SSS_LINK_ANCHOR3').click()
        

    def waitForEnrollmentWindow(self, year):
        if(int(year) == 1):  # freshman
            startDate = Preferences.freshStart
        if(int(year) == 2):  # sophomore
            startDate = Preferences.sophoStart
        if(int(year) == 3):  # junior
            startDate = Preferences.juniorStart
        if(int(year) == 4):  # senior
            startDate = Preferences.seniorStart
        waiting = True

        # Wait until course enroll 'opens' then keep refresh until
        # 'select classes to add' page loads.
        while(waiting):
            if (startDate < datetime.datetime.now()):
                waiting = False
                self.driver.execute_script('location.reload()')
                loaded = False

                while(not loaded):
                    src = self.driver.page_source
                    if('Select classes to add' in src):
                        loaded = True
                        logging.warning(
                            'BOT @' + str(self.className) + ': Enrollment window is open')
                        break
                    with wait_for_page_load(self.driver):
                        self.driver.refresh()
                        logging.warning(
                            'BOT @' + str(self.className) + ': Hard Refresh')

            # Print time remaing until start
            t = startDate - datetime.datetime.now()
            stdout.write('Time remaining until start: %s%%   \r' % (t))
            stdout.flush()

    def selectSemester(self):
        # Select Semester
        xpath = '//*[@id="SSR_DUMMY_RECV1$sels$2$$0"]'
        try:
            self.driver.find_element_by_xpath(xpath).click()
        except Exception:
            logging.exception(
                'BOT @' + str(self.className) + ': Cannot find semester')

        with wait_for_page_load(self.driver):
            self.driver.find_element_by_id('DERIVED_SSS_SCT_SSR_PB_GO').click()
        logging.warning('BOT @' + str(self.className) + ': Selected semester')

    def enterClassNbr(self):
        # Enter class nbr on main 'add' page
        self.driver.find_element_by_id(
            'DERIVED_REGFRM1_CLASS_NBR').send_keys(self.className)
        with wait_for_page_load(self.driver, 'Select classes to add'):
            self.driver.find_element_by_id(
                'DERIVED_REGFRM1_SSR_PB_ADDTOLIST2$9$').click()
        logging.warning(
            'BOT @' + str(self.className) + ': Entered class Nbr semester')
        src = self.driver.page_source
        if('The class number entered is a duplicate. Try another' in src):
            logging.error('BOT @' + str(self.className) +
                          ': The class number eneted is a duplicate. Proceeding to compelte enrollment')
            self.driver.save_screenshot(
                'bot_' + str(self.className) + '_error_screenshot_' + str(self._screentShotCount) + '.png')
            self._screentShotCount += 1
            self.completeEnrollment()

    def clickNextToHome(self, count=0):
        # Click next until we get to the home page
        src = self.driver.page_source
        if('has been added to your Shopping Cart' in src):
            return
        if (count > 10):
            self.driver.save_screenshot(
                'bot_' + str(self.className) + '_error_screenshot_' + str(self._screentShotCount) + '.png')
            self._screentShotCount += 1
            logging.error('BOT @' + str(self.className) +
                          ': Failed to return home after 10 clicks. Screenshot Saved')

        logging.warning('BOT @' + str(self.className) + ': Clicking next')
        # FIX ME, this wait?
        with wait_for_page_load(self.driver, 'Select classes to add'):
            try: 
                self.driver.find_element_by_xpath('//a[contains(@id, "DERIVED_CLS_DTL_NEXT_PB")]').click()
            except Exception as e:
                print e
                logging.warning('BOT @' + str(self.className) + ': Could not find home button, attempting to contiune')
                return
        return self.clickNextToHome(count + 1)

    def completeEnrollment(self):
        # finish clicking to the end, don't actually enroll if in test mode
        #with wait_for_page_load(self.driver):
        try:    
            self.driver.find_element_by_xpath(
                    '//a[contains(@id, "DERIVED_REGFRM1_LINK_ADD_ENRL")]').click()
            src = self.driver.page_source
            if('Finish Enrolling to process your request for the classes listed below' not in src):
                self.driver.save_screenshot(
                    'bot_' + str(self.className) + '_error_screenshot_' + str(self._screentShotCount) + '.png')
                self._screentShotCount += 1
                logging.error('BOT @' + str(self.className) +
                              ': Failed to Proceed to Step 2 will try to remove classes and try again. Screenshot Saved')

            logging.warning(
                'BOT @' + str(self.className) + ': On final page, ready to enroll')
            if (not self._testMode):
                with wait_for_page_load(self.driver):
                    self.driver.find_element_by_id(
                        'DERIVED_REGFRM1_SSR_PB_SUBMIT').click()
                src = self.driver.page_source
                if('Error: Unable to complete your request' in src):
                    self.driver.save_screenshot(
                        'bot_' + str(self.className) + '_error_screenshot_' + str(self._screentShotCount) + '.png')
                    self._screentShotCount += 1
                    logging.error('BOT @' + str(self.className) +
                                  ': Failed to Finish Enrolling. Screenshot Saved')
                else:
                    logging.warning(
                        'BOT @' + str(self.className) + ': Enrollment complete')
            else:
                logging.warning(
                    'BOT @' + str(self.className) + ': Test Mode, did not compelte enorllment')

            _time = time.time() - self._start
            logging.warning(
                'BOT @' + str(self.className) + ': Time to complete: ' + str(_time))

            # keep trying if on repeat
            if self.repeat:
                with wait_for_page_load(self.driver, text='status report for enrollment'):
                    self.driver.find_element_by_xpath(
                    '//a[contains(@id, "DERIVED_REGFRM1_SSR_LINK_STARTOVER")]').click()
                time.sleep(.3)
                self.completeEnrollment()
        
        except Exception as e:
            print 'go home', str(e)
            logging.error('BOT @' + str(self.className) +
                          'Error completeing enrollment, returning home')
            logging.error('BOT @' + str(self.className) +
                          'Error: ' + str(e))
            self.goHome()
            self.selectSemester()
            self.completeEnrollment()


    def addDiscussion(self, discussion, only):
        #time.sleep(4) # FIXME: this didn't wait to load. What clicks this?
        with wait_for_page_load(self.driver, extraXpath='//*[@id="SSR_CLS_TBL_RE_CLASS_NBR$1"]'):
            pass

        if (only):
            xpath = '//*[@id="SSR_CLS_TBL_RE_CLASS_NBR$'
            buttonpath = '//*[@id="SSR_CLS_TBL_RE$sels$' # '(number)$$0"]'
            table = 'RE'
        else:
            xpath = '//*[@id="SSR_CLS_TBL_R1_CLASS_NBR$'
            buttonpath = '//*[@id="SSR_CLS_TBL_R1$sels$' # '(number)$$0"]'
            table = 'R1'
        try:
            if (only):
                length = int(str(self.driver.find_element_by_xpath(
                    '//*[@id="SSR_CLS_TBL_RE$scroll$0"]/tbody/tr[2]/td/span[3]').text)[-2:])
                tablelength = int(str(self.driver.find_element_by_xpath(
                    '//*[@id="SSR_CLS_TBL_RE$scroll$0"]/tbody/tr[2]/td/span[3]').text)[2:3])
            else:
                length = int(str(self.driver.find_element_by_xpath(
                    '//*[@id="SSR_CLS_TBL_R1$scroll$0"]/tbody/tr[3]/td/span[2]').text)[-2:])
                tablelength = int(str(self.driver.find_element_by_xpath(
                    '//*[@id="SSR_CLS_TBL_R1$scroll$0"]/tbody/tr[3]/td/span[2]').text)[2:3])
            logging.warning(
                'BOT @' + str(self.className) + ': Found discussion length and table-length ')
        except:
                # Over-estimate in case we cannot find the table length
            length = 20
            tablelength = 20
            logging.warning('BOT @' + str(self.className) +
                            ': Could not find discussion table-length. Using defaults')

        _found = False
        for i in range(0, tablelength):
            try:
                e = self.driver.find_element_by_xpath(
                    (xpath + str(i) + '"]' )).text
                if (str(e) == str(discussion)):
                    _found = True
                    self.driver.find_element_by_xpath(
                        buttonpath + str(i) + '$$0"]' ).click()
                    break
            except Exception as e:
                print e
                continue
        x = 5
        while(x < length and not _found):
            self.driver.find_element_by_name(
                'SSR_CLS_TBL_' + table + '$fdown$img$0').click()
            for i in range(2, tablelength + 2):
                try:
                    e = self.driver.find_element_by_xpath(
                        (xpath + str(i) + '"]' )).text
                    if (str(e) == str(discussion)):
                        _found = True
                        self.driver.find_element_by_xpath(
                            buttonpath + str(i) + '$$0"]' ).click()
                        break
                except:
                    continue
            x += 5
        logging.warning(
            'BOT @' + str(self.className) + ': Successfully selected discussion')

    def addLab(self, lab, only):
         # FIXME: do xpaths like the disccusion section
        if (only):
            xpath = '//*[@id="SSR_CLS_TBL_RE$scroll$0"]/tbody/tr[1]/td/table/tbody/tr['
            table = 'RE'
        else:
            xpath = '//*[@id="SSR_CLS_TBL_R2$scroll$0"]/tbody/tr[2]/td/table/tbody/tr['
            table = 'R2'
        try:
            if (only):
                length = int(str(self.driver.find_element_by_xpath(
                    '//*[@id="SSR_CLS_TBL_RE$scroll$0"]/tbody/tr[2]/td/span[3]').text)[-2:])
                tablelength = int(str(self.driver.find_element_by_xpath(
                    '//*[@id="SSR_CLS_TBL_RE$scroll$0"]/tbody/tr[2]/td/span[3]').text)[2:3])
            else:
                length = int(str(self.driver.find_element_by_xpath(
                    '//*[@id="SSR_CLS_TBL_R1$scroll$0"]/tbody/tr[3]/td/span[2]').text)[-2:])
                tablelength = int(str(self.driver.find_element_by_xpath(
                    '//*[@id="SSR_CLS_TBL_R1$scroll$0"]/tbody/tr[3]/td/span[2]').text)[2:3])
            logging.warning(
                'BOT @' + str(self.className) + ': Found lab length and table-length ')
        except:
                # Over-estimate in case we cannot find the table length
            length = 20
            tablelength = 20
            logging.warning('BOT @' + str(self.className) +
                            ': Could not find lab table-length. Using defaults')

        _found = False
        for i in range(2, tablelength + 2):
            try:
                e = self.driver.find_element_by_xpath(
                    xpath + str(i) + ']/td[2]/span').text
                if (str(e) == str(lab)):
                    _found = True
                    self.driver.find_element_by_xpath(
                        xpath + str(i) + ']/td[1]/input').click()
                    break
            except:
                continue
        x = 5
        while(x < length and not _found):
            self.driver.find_element_by_name(
                'SSR_CLS_TBL_' + table + '$fdown$img$0').click()
            for i in range(2, tablelength + 2):
                try:
                    e = self.driver.find_element_by_xpath(
                        (xpath + str(i) + ']/td[2]/span')).text
                    if (str(e) == str(lab)):
                        _found = True
                        self.driver.find_element_by_xpath(
                            xpath + str(i) + ']/td[1]/input').click()
                        break
                except:
                    continue
            x += 5
        logging.warning(
            'BOT @' + str(self.className) + ': Successfully selected lab')


if __name__ == '__main__':
    if len(sys.argv) != 4 and len(sys.argv) != 3:
        print 'Wrong number of args!'
        print "Please run the command: python src/bot.py <netid> <classtoadd> <disscusion (optional)>"
        sys.exit(1)

    b = Bot()

    # Get username
    netid = str(sys.argv[1])

    # Get password
    password = getpass.getpass("Password:")

    # Get class number
    classnumber = str(sys.argv[2])

    # Get section number
    if len(sys.argv) == 4:
        secnumber = str(sys.argv[3])
        b.addClass(netid, password, classnumber, secnumber, repeat=True)
    else:
        b.addClass(netid, password, classnumber, repeat=True)
