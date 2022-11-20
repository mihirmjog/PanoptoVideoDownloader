from selenium import webdriver as WD
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
#import time

class APIEndpointFinder:
    '''Provides a list of the relevant API Endpoint URLs used by the Panapoto Video Player'''
    
    def __init__(self):
        chrome_options = WD.ChromeOptions()
        chrome_options.add_argument("user-data-dir=C:/Users/mihir/AppData/Local/Google/Chrome/User Data")
        chrome_options.add_argument("remote-debugging-port=9222")
        self.WebDriver = WD.Chrome(options = chrome_options)
        self.WebDriver.maximize_window()

    def get_URL_list(self, panopto_video_URL): 
        endpoint_URL_list = []


        self.WebDriver.get(panopto_video_URL)
        self.__kerberos_login__() 

        while (True): #Waits until video player is accessible to Selenium. Can create infinite loop.
            try: 
                self.__play_video__() 
                self.__mute_video__()
            except:
                continue
            else:
                break
                
        if self.__check_for_camera_expander__():
            camera_expander_button = self.WebDriver.find_element(By.ID, "selectedSecondary")
            self.__click_through_all_cameras__(camera_expander_button, True)
        else:
            self.__click_through_all_cameras__(None, False)
        
        return endpoint_URL_list

    def __kerberos_login__(self):
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

    def __check_for_camera_expander__(self):
        has_flyout_button =  self.WebDriver.find_element(By.ID, "selectedSecondary").is_displayed()
        self.__escape__()

        return has_flyout_button

    def __play_video__(self): 
        play_button = self.WebDriver.find_element(By.CSS_SELECTOR, "#playButton") 
        
        if play_button.get_attribute("class") == "transport-button paused":
            play_button.click()

        return

    def __click_through_all_cameras__(self, camera_expander_button, has_camera_expander):
        if has_camera_expander:
            list_of_potential_camera_buttons = self.WebDriver.find_element(By.ID, "secondaryExpander").find_elements(By.TAG_NAME, "div")
        else:
            list_of_potential_camera_buttons = self.WebDriver.find_element(By.ID, "transportControls").find_elements(By.TAG_NAME, "div")
        
        for potential_camera_button in list_of_potential_camera_buttons:
            if potential_camera_button.get_attribute("class") == "player-tab-header transport-button accented-tab object-video secondary-header":
                if has_camera_expander:
                    camera_expander_button.click()
                if potential_camera_button.is_displayed():
                    potential_camera_button.click()
                    self.__escape__()
        
        return

    def __escape__(self):
        WD.ActionChains(self.WebDriver).send_keys(Keys.ESCAPE).perform()

        return 

