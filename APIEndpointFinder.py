from selenium import webdriver as WD
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import selenium.webdriver.common.devtools.v107 as Devtools
#import time

class APIEndpointFinder:
    '''Provides a list of the relevant API Endpoint URLs used by the Panapoto Video Player'''
    
    def __init__(self):
        chrome_options = WD.ChromeOptions()
        chrome_options.add_argument("user-data-dir=C:/Users/mihir/AppData/Local/Google/Chrome/User Data")
        chrome_options.add_argument("remote-debugging-port=9222")   
        self.WebDriver = WD.Chrome(options = chrome_options)
        self.__endpoint_URL_list__ = []

        self.WebDriver.maximize_window()
        Devtools.network.enable()

    def get_URL_list(self, panopto_video_URL): 
        self.endpoint_URL_list = []
        
        #Devtools.network
        self.WebDriver.get(panopto_video_URL)
        self.__login_to_kerberos__()

        while True: #Waits until controls of video player are accessible to Selenium. #TODO Prevent potential infinite loop
            try: 
                self.__play_video__() 
                self.__mute_video__()
            except:
                continue
            else:
                break
                
        if self.WebDriver.find_element(By.ID, "selectedSecondary").is_displayed(): #Checks if the panapto video has a camera expander
            self.__click_through_camera_expander__()
        else: #Video player does not have camera expander
            self.__click_through_all_cameras__()
        #TODO Check if num_cameras equals number of clicks, throw exception otherwise
        return self.__endpoint_URL_list__

    def __login_to_kerberos__(self):
        try: 
            login_button = self.WebDriver.find_element(By.NAME, "Submit")
            login_button.click()
        finally: 
            return 

    def __mute_video__(self):
        volumeControl_elem = self.WebDriver.find_element(By.XPATH, "/html/body/form/div[3]/div[10]/div[8]/main/div/div[4]/div/div[1]/div[8]/div[1]")
        if volumeControl_elem.get_attribute("title") == "Mute":
            volumeControl_elem.click()

        return 

    def __play_video__(self): 
        play_button = self.WebDriver.find_element(By.CSS_SELECTOR, "#playButton") 
        
        if play_button.get_attribute("class") == "transport-button paused":
            play_button.click()

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

    def __is_camera_button__(self, potential_camera_button):
        return potential_camera_button.get_attribute("class") == "player-tab-header transport-button accented-tab object-video secondary-header"
    
    #def __add_endpoint_URL__(self): 
    #
    #    return 0
