import time
from preferences import Preferences

class wait_for_page_load(object):

    def __init__(self, browser, text=None, extraXpath=None):
        self.browser = browser
        self.escape_text = text
        self.extraXpath = extraXpath

    def __enter__(self):
        self.old_page = self.browser.find_element_by_tag_name('html')

    def wait_for(self, condition_function):
        start_time = time.time()
        while (time.time() < start_time + Preferences.botTimeout):
            if condition_function():
                return True
            elif self.escape_text and len(self.browser.find_elements_by_xpath("//*[contains(text(), '" + str(self.escape_text) +"')]")) > 0:
                if self.extraXpath is not None:
                    if self.browser.find_elements_by_xpath(self.extraXpath):
                        return True
                else:
                    return True
            else:
                time.sleep(0.1)
        return True
        raise Exception(
            'Timeout waiting for {}'.format(condition_function.__name__)
        )

    def page_has_loaded(self):
        new_page = self.browser.find_element_by_tag_name('html')
        return new_page.id != self.old_page.id

    def __exit__(self, *_):
        self.wait_for(self.page_has_loaded)
