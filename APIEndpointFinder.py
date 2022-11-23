from selenium import webdriver as WD
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import *
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import json

class APIEndpointFinder:
    '''Provides a list of the relevant API Endpoint URLs used by the Panapoto Video Player'''
    
    def __init__(self):
        chrome_capabilities = DesiredCapabilities.CHROME.copy()
        chrome_capabilities["goog:loggingPrefs"] = {"performance": "ALL"}
        chrome_options = WD.ChromeOptions()
        chrome_options.add_argument("user-data-dir=C:/Users/mihir/AppData/Local/Google/Chrome/User Data") #Need to use preexisting chrome profile to autofill kerberos credentials and bypass 2FA
        chrome_options.add_argument("remote-debugging-port=9222")   
        chrome_options.add_experimental_option('perfLoggingPrefs', {
            'enableNetwork': True
            }) 
        self.WebDriver = WD.Chrome(options = chrome_options, desired_capabilities= chrome_capabilities)
        
        self.WebDriver.maximize_window()

    def get_URL_list(self, panopto_video_URL): 
        #clear
        self.WebDriver.get(panopto_video_URL)

        self.__login_to_kerberos__()
        self.__mute_video__()
        self.__play_video__() 

        if self.WebDriver.find_element(By.ID, "selectedSecondary").is_displayed(): #Checks if the panapto video has a camera expander
            self.__click_through_camera_expander__()
        else: #Video player does not have camera expander
            self.__click_through_all_cameras__()
        
        webdriver_logs = self.WebDriver.get_log('performance')
        #TODO Check if num_cameras equals number of clicks, throw exception otherwise
        endpoint_URL_list = self.__create_endpoint_URL_list__(webdriver_logs)

        return endpoint_URL_list

    def __login_to_kerberos__(self):
        try: 
            login_button = self.WebDriver.find_element(By.NAME, "Submit")
            login_button.click()
        finally: 
            return 

    def __mute_video__(self):
        volume_control_button = self.__wait_until_element_is_clickable__(By.XPATH, "/html/body/form/div[3]/div[10]/div[8]/main/div/div[4]/div/div[1]/div[8]/div[1]")
        
        if volume_control_button.get_attribute("title") == "Mute":
            volume_control_button.click()

        return 

    def __play_video__(self): 
        play_video_button = self.__wait_until_element_is_clickable__(By.CSS_SELECTOR, "#playButton")

        if play_video_button.get_attribute("class") == "transport-button paused":
            play_video_button.click()

        return

    def __click_through_camera_expander__(self):
        camera_expander_button = self.WebDriver.find_element(By.ID, "selectedSecondary")
        list_of_potential_camera_buttons = self.WebDriver.find_element(By.ID, "secondaryExpander").find_elements(By.TAG_NAME, "div")

        for potential_camera_button in list_of_potential_camera_buttons:
            if self.__is_camera_button__(potential_camera_button):
                camera_expander_button.click()
                potential_camera_button.click() 
                WD.ActionChains(self.WebDriver).send_keys(Keys.ESCAPE).perform() #Closes camera expander

        return

    def __click_through_all_cameras__(self):
        list_of_potential_camera_buttons = self.WebDriver.find_element(By.ID, "transportControls").find_elements(By.TAG_NAME, "div")
        
        for potential_camera_button in list_of_potential_camera_buttons:
            if self.__is_camera_button__(potential_camera_button) and potential_camera_button.is_displayed():
                    potential_camera_button.click()

        return

    def __wait_until_element_is_clickable__(self, locator, element):
        target_element = WebDriverWait(self.WebDriver, 10, poll_frequency=1, ignored_exceptions=[ElementNotVisibleException, ElementNotSelectableException]).until(
            EC.element_to_be_clickable((locator, element))
        )

        return target_element

    def __is_camera_button__(self, potential_camera_button):
        return potential_camera_button.get_attribute("class") == "player-tab-header transport-button accented-tab object-video secondary-header"
    
    def __create_endpoint_URL_list__(self, webdriver_logs): 
        endpoint_URL_list = []
        for log in webdriver_logs:
            print(log)
        return        