from selenium import webdriver as WD
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import *
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

class ConfiguredWD(WD.Chrome):
    '''Subclassed WebDriver configured with user profile.'''
    def __init__(self, logging):
        chrome_options = WD.ChromeOptions()
        chrome_options.add_argument("user-data-dir=C:/Users/mihir/AppData/Local/Google/Chrome/User Data") 
        chrome_options.add_argument("remote-debugging-port=9222") 
        if logging:
            chrome_capabilities = DesiredCapabilities.CHROME.copy()
            chrome_capabilities["goog:loggingPrefs"] = {
            "performance"        : "ALL",
            "level"              : "INFO"}
            chrome_options.add_experimental_option('perfLoggingPrefs', {
            'traceCategories': 'devtools.Network.requestWillBeSent',
            'enablePage'     : False
            })
            self.__ConfiguredWD = super().__init__(options = chrome_options, desired_capabilities= chrome_capabilities)
        else:
            self.__ConfiguredWD = super().__init__(options = chrome_options)
        
        self.maximize_window()
        

    def wait_for_clickable_element(self, locator, element):
        target_element = WebDriverWait(self, 10, poll_frequency=1, ignored_exceptions=[ElementNotVisibleException, ElementNotSelectableException]).until(
            EC.element_to_be_clickable((locator, element))
        )

        return target_element

        

