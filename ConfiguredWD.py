from selenium import webdriver as WD
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import *
#from selenium.webdriver.common.log import * #TODO: Remove global import


class ConfiguredWD(WD.Chrome):
    '''Subclassed WebDriver configured with user profile.'''

    def __init__(self, logging):
        #TODO Start in new browser window
        chrome_options = WD.ChromeOptions()
        chrome_options.add_argument("user-data-dir=C:/Users/mihir/AppData/Local/Google/Chrome/User Data") 
        chrome_options.add_argument(r"C:\Users\mihir\AppData\Local\Google\Chrome\User Data\Profile 1")
        if logging:
            chrome_options.set_capability("goog:loggingPrefs", {
                                                                    'performance'        : 'ALL'})
            chrome_options.add_experimental_option("perfLoggingPrefs", {
                                                                            "traceCategories" : "devtools.Network.requestWillBeSent"})
            
        chrome_service = WD.ChromeService(executable_path = r"C:\Users\mihir\Documents\Git\VideoDownloader\bin\chromedriver.exe")
        super().__init__(options = chrome_options, service = chrome_service) 
        self.maximize_window()
        
    def get_element_when_accessible(self, locator, element):
        target_element = WebDriverWait(self, 5, poll_frequency=1, ignored_exceptions=[ElementNotVisibleException, ElementNotSelectableException]).until(
            EC.element_to_be_clickable((locator, element)) 
        )
        
        while not target_element.is_displayed():
            continue

        return target_element