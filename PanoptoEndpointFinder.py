from selenium import webdriver as WD
from selenium.webdriver.common.by import By
from selenium.common.exceptions import *
from selenium.webdriver.common.keys import Keys
import json
import ConfiguredWD as Configured_WD
from time import sleep
#TODO Determine what Seleniun dependencies should be deleted
class PanoptoEndpointFinder: 
    '''Provides a list of the relevant API Endpoint URLs used by the Panapoto Video Player'''
    
    def __init__(self):  
        self.__WebDriver = Configured_WD.ConfiguredWD(logging = True)
        self.__num_of_cameras = -1
        

    def get_URL_list(self, panopto_video_URL): 
        self.__num_of_cameras = 0
        self.__WebDriver.get_log('browser')  #clears browser performance logs
        self.__WebDriver.get(panopto_video_URL)

        self.__login_to_kerberos()
        self.__mute_video()
        self.__play_video() 

        if self.__WebDriver.find_element(By.ID, "selectedSecondary").is_displayed(): #Checks if the panapto video has a camera expander
            self.__click_through_camera_expander()
        else: #Video player does not have camera expander
            self.__click_through_all_cameras()
        
        webdriver_logs = self.__WebDriver.get_log('performance')
        list_of_endpoint_URLs = self.__create_endpoint_URLs_list(webdriver_logs)
        #self.__check_if_num_of_cameras_is_correct(list_of_endpoint_URLs) #Raises exception if false
        self.__WebDriver.quit()

        return list_of_endpoint_URLs

    def __login_to_kerberos(self):
        sleep(1)
        try: 
            login_button = self.__WebDriver.find_element(By.NAME, "Submit")
            login_button.click()
        finally: 
            return 

    def __mute_video(self):
        volume_control_button = self.__WebDriver.get_element_when_accessible(By.XPATH, "/html/body/form/div[3]/div[10]/div[8]/main/div/div[4]/div/div[1]/div[8]/div[1]")
        
        if volume_control_button.get_attribute("title") == "Mute":
            volume_control_button.click()

    def __play_video(self): 
        play_video_button = self.__WebDriver.get_element_when_accessible(By.CSS_SELECTOR, "#playButton")

        if play_video_button.get_attribute("class") == "transport-button paused":
            play_video_button.click()

    def __click_through_camera_expander(self):
        camera_expander_button = self.__WebDriver.find_element(By.ID, "selectedSecondary")
        list_of_potential_camera_buttons = self.__WebDriver.find_element(By.ID, "secondaryExpander").find_elements(By.TAG_NAME, "div")

        for potential_camera_button in list_of_potential_camera_buttons:
            if self.__is_camera_button(potential_camera_button):
                camera_expander_button.click()
                potential_camera_button.click()
                sleep(1) 
                self.__num_of_cameras += 1
                WD.ActionChains(self.__WebDriver).send_keys(Keys.ESCAPE).perform() #Closes camera expander

    def __click_through_all_cameras(self):
        list_of_potential_camera_buttons = self.__WebDriver.find_element(By.ID, "transportControls").find_elements(By.TAG_NAME, "div")
        
        for potential_camera_button in list_of_potential_camera_buttons:
            if not self.__is_camera_button(potential_camera_button):
                continue

            elif potential_camera_button.is_displayed():
                self.__num_of_cameras += 1
                potential_camera_button.click()
                sleep(1)

    def __create_endpoint_URLs_list(self, webdriver_logs): 
        set_of_endpoint_URLs = set()
        
        for log in webdriver_logs:
            if "index.m3u8" not in log['message']:
                continue
                
            if "index.m4a" in log['message']:
                continue
            
            log_message = json.loads(log['message'])
            #TODO Remove try/else block
            try:
                endpoint_URL = set_of_endpoint_URLs.add(log_message['message']['params']['request']['url'])
            except:
                continue
            else:
                if endpoint_URL is not None:
                    set_of_endpoint_URLs.add(endpoint_URL)
                    
        list_of_endpoint_URLs = list(set_of_endpoint_URLs)

        return list_of_endpoint_URLs

    def __check_if_num_of_cameras_is_correct(self, list_of_endpoint_URLs):
        if len(list_of_endpoint_URLs) == 0:
            raise Exception("No endpoints found!")
        elif len(list_of_endpoint_URLs) == (self.__num_of_cameras + 1):
            return
        else:
            raise Exception("Incorrect number of cameras for the URL:" + self.__WebDriver.current_url)

    def __is_camera_button(self, potential_camera_button):
        is_camera = potential_camera_button.get_attribute("class").__contains__("player-tab-header transport-button accented-tab object-video secondary-header")
        
        return is_camera