#!/usr/bin/env python

import time
import datetime
import logging
from sys import stdout
from preferences import Preferences
import warnings
from wait import wait_for_page_load
from selenium import webdriver


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

    def addClass(self, netid, password, className, discussion=None, lab=None, test=False):
        self._testMode = test
        self.className = className
        logging.warning('BOT @' + str(self.className) + ': Bot initailized')
        # define settings from preference file #
        self.getPreferences(password)

        url = 'http://studentcenter.cornell.edu/'
        #requests.get(
            #'http://studentcenter.cornell.edu', allow_redirects=True).url

        # LOG INTO STUDENT CENTER
        self.logIntoStudentCenter(url, netid, password)

        # SELECT SEMESTER
        self.selectSemester()

        # WAIT FOR APPOINTMENT
        self.waitForEnrollmentWindow(Preferences.gradeLevel)

        self._start = time.time()

        # ENTER CLASS NBR
        self.enterClassNbr()

        # Handle adding disscusion and/or lab
        if (discussion != None and self.is_integer(discussion)):
            if (lab != None and self.is_integer(lab)):
                logging.warning(
                    'BOT @' + str(self.className) + ': Trying to add discussion and lab')
                self.addDiscussion(discussion, only=False)
                self.addLab(lab, only=False)
            else:
                logging.warning(
                    'BOT @' + str(self.className) + ': Trying to add discussion')
                self.addDiscussion(discussion, only=True)
        elif (lab != None and self.is_integer(lab)):
            logging.warning(
                'BOT @' + str(self.className) + ': Trying to add lab')
            self.addLab(lab, only=True)

        # Click next until we get back to the home page
        self.clickNextToHome()

        # PROCEED to Complete Enrollment
        self.completeEnrollment()

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
            year = Preferences.gradeLevel
        else:
            warnings.warn(
                'Invalid Grade Level preferences. Using freshman by default')
            year = 1

    def logIntoStudentCenter(self, url, netid, password):
        # Log into Student Center
        self.driver.get(url)
        self.driver.find_element_by_id('netid').send_keys(netid)
        if (password != ''):
            self.driver.find_element_by_id('password').send_keys(password)
            with wait_for_page_load(self.driver):
                self.driver.find_element_by_name('Submit').click()
        logging.warning(
            'BOT @' + str(self.className) + ': Logged into Student Center')
        self.driver.find_element_by_id('DERIVED_SSS_SCL_LINK_ADD_ENRL').click()

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
                # keep track of how long app took to get class
                _time = time.time()
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
        xpath = '//*[@id="SSR_DUMMY_RECV1$scroll$0"]/tbody/tr[3]/td[1]/input'
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
            'DERIVED_REGFRM1_CLASS_NBR$42$').send_keys(self.className)
        with wait_for_page_load(self.driver):
            self.driver.find_element_by_id(
                'DERIVED_REGFRM1_SSR_PB_ADDTOLIST2$44$').click()
        logging.warning(
            'BOT @' + str(self.className) + ': Entered class Nbr semester')
        src = self.driver.page_source
        if('The class number entered is a duplicate.  Try another'):
            logging.error('BOT @' + str(self.className) +
                          ': The class number eneted is a duplicate. Proceeding to compelte enrollment')
            self.driver.save_screenshot(
                'bot_' + str(self.className) + '_error_screenshot_' + str(self._screentShotCount) + '.png')
            self._screentShotCount += 1
            self.completeEnrollment()

    def clickNextToHome(self):
        # Click next until we get to the home page
        _home = False
        count = 0
        while(not _home):
            logging.warning('BOT @' + str(self.className) + ': Clicking next')
            count += 1
            with wait_for_page_load(self.driver):
                self.driver.find_element_by_id(
                    'DERIVED_CLS_DTL_NEXT_PB').click()
            src = self.driver.page_source
            if('your Shopping Cart and when you are satisfied' in src):
                _home = True
            if (count > 10):
                driver.save_screenshot(
                    'bot_' + str(self.className) + '_error_screenshot_' + str(self._screentShotCount) + '.png')
                self._screentShotCount += 1
                logging.error('BOT @' + str(self.className) +
                              ': Failed to return home after 10 clicks. Screenshot Saved')

    def completeEnrollment(self):
        # finish clicking to the end, don't actually enroll if in test mode
        with wait_for_page_load(self.driver):
            self.driver.find_element_by_id(
                'DERIVED_REGFRM1_LINK_ADD_ENRL').click()
        src = self.driver.page_source
        if('Finish Enrolling to process your request for the classes listed below' not in src):
            self.driver.save_screenshot(
                'bot_' + str(self.className) + '_error_screenshot_' + str(self._screentShotCount) + '.png')
            self._screentShotCount += 1
            logging.error('BOT @' + str(self.className) +
                          ': Failed to Proceed to Step 2 will try to remove classes and try again. Screenshot Saved')
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

        _time = time.time() - self._start
        logging.warning(
            'BOT @' + str(self.className) + ': Time to complete: ' + str(_time))

        if (self._testMode):
            time.sleep(1)
        else:
            time.sleep(10)

        self.driver.close()

    def addDiscussion(self, discussion, only):
        if (only):
            xpath = '//*[@id="SSR_CLS_TBL_RE$scroll$0"]/tbody/tr[1]/td/table/tbody/tr['
            table = 'RE'
        else:
            xpath = '//*[@id="SSR_CLS_TBL_R1$scroll$0"]/tbody/tr[2]/td/table/tbody/tr['
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
        for i in range(2, tablelength + 2):
            try:
                e = self.driver.find_element_by_xpath(
                    (xpath + str(i) + ']/td[2]/span')).text
                if (str(e) == str(discussion)):
                    _found = True
                    self.driver.find_element_by_xpath(
                        xpath + str(i) + ']/td[1]/input').click()
                    break
            except:
                continue
        x = 5
        while(x < length and _found == False):
            self.driver.find_element_by_name(
                'SSR_CLS_TBL_' + table + '$fdown$img$0').click()
            for i in range(2, tablelength + 2):
                try:
                    e = self.driver.find_element_by_xpath(
                        (xpath + str(i) + ']/td[2]/span')).text
                    if (str(e) == str(discussion)):
                        _found = True
                        self.driver.find_element_by_xpath(
                            xpath + str(i) + ']/td[1]/input').click()
                        break
                except:
                    continue
            x += 5
        logging.warning(
            'BOT @' + str(self.className) + ': Successfully selected discussion')

    def addLab(self, lab, only):
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
        while(x < length and _found == False):
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
