import PanoptoEndpointFinder as PEF
import queue
import pathlib
from selenium.webdriver.common.by import By
from selenium.common.exceptions import *
import subprocess
import ConfiguredWD as Configured_WD
from time import sleep
import os
from selenium.webdriver import ActionChains

#TODO Determine what Seleniun dependencies should be deleted

class Driver: 
    '''Driver Class'''

    def __init__(self):
        subprocess.Popen(['C:\Program Files\JDownloader\JDownloader\JDownloader2.exe'], stdout=subprocess.PIPE)
        self.__DownloadQueue = queue.Queue()        
        self.__PanoptoEndpointFinder = PEF.PanoptoEndpointFinder()
        self.__download_location = None
        self.__set_of_download_URLs = set()
        self.__error_log_dict = {} #TODO Add try/except block where failed download URLs (potentially from incorrent num_of_cameras) are printed to console or in a log.txt
        #TODO Check length of video?
        

    def set_download_location(self, download_location): 
        target_directory = pathlib.Path(pathlib.PureWindowsPath(download_location).as_posix())
        self.__create_directory(target_directory)
        target_directory = self.__append_to_filepath(target_directory, "/") #TODO Place slash before folder_name
        self.__download_location = target_directory


    def add(self, folder_name, video_URL):
        if self.__download_location == None:
            raise Exception("Set Download Location first!")
        elif video_URL in self.__set_of_download_URLs:
            raise Exception("Download URL already added!")
        else: 
            self.__set_of_download_URLs.add(video_URL)

        relative_folder_name = "/" + folder_name
        download_directory = self.__append_to_filepath(self.__download_location, relative_folder_name)
        self.__create_directory(download_directory)

        if "panopto.com" in video_URL:
            try:
                list_of_panopto_endpoints = self.__PanoptoEndpointFinder.get_URL_list(video_URL)
            except:
                self.__error_log_dict[video_URL] = None #TODO Add actual error messages as value
            else:    
                for panopto_endpoint in list_of_panopto_endpoints:
                    download_item = (download_directory, panopto_endpoint)
                    self.__DownloadQueue.put(download_item)
        else:
            download_item = (download_directory, video_URL)
            self.__DownloadQueue.put(download_item)
    
    def start_downloads(self):
        self.__PanoptoEndpointFinder.close_finder()
        self.__WebDriver = Configured_WD.ConfiguredWD(logging = False)
        self.__WebDriver.get("https://my.jdownloader.org")
        self.__go_to_my_JDownloader()
        
        while self.__DownloadQueue:
            current_download_item = self.__DownloadQueue.get()
            (download_dir_for_current_item, current_download_URL) = current_download_item
            try:
                self.__download_current_item(download_dir_for_current_item, current_download_URL)
            except:
                self.__error_log_dict[current_download_URL] = None #TODO Add actual error messages as value
        self.__WebDriver.close()
        self.__print_status()

    
    def __create_directory(self, target_directory):
        target_directory.mkdir(parents=True, exist_ok= True)

    def __download_current_item(self, download_dir, download_URL):
        #TODO Check if sleep functions are necessary
        self.__click_on_add_new_link()
        self.__type_in_download_URL(download_URL)
        self.__type_in_new_download_location(download_dir)
        self.__wait_until_download_is_added()
        self.__start_download_for_current_item()
        #self.__check_for_error()
        while not self.__has_nfo_file(download_dir):
            sleep(0.5)
            continue
        return

    def __append_to_filepath(self, original_filepath, path_to_append_as_str):
        original_filepath_as_str = original_filepath.__str__()
        new_filepath_as_string = original_filepath_as_str + path_to_append_as_str
        new_filepath = pathlib.Path(pathlib.PureWindowsPath(new_filepath_as_string).as_posix())

        return new_filepath

    def __go_to_my_JDownloader(self):
        my_jdownloader_button = self.__WebDriver.get_element_when_accessible(By.XPATH, "/html/body/div[1]/div[2]/div/div/div[2]/div[1]/div[2]/div/div/div/img")
        my_jdownloader_button.click()


    def __click_on_add_new_link(self):
        current_URL = self.__WebDriver.current_url
        link_collector_URL = current_URL.replace(":downloads", ":links")
        self.__WebDriver.get(link_collector_URL)
        add_links_button = self.__WebDriver.get_element_when_accessible(By.XPATH, "//*[contains(text(),'Add links')]")
        add_links_button.click()
        sleep(1)

    def __type_in_download_URL(self, download_URL):
        download_URL_textbox = self.__WebDriver.get_element_when_accessible(By.XPATH, "/html/body/div[4]/div/div/div/div/table/tbody/tr[1]/td[2]/div[1]/textarea")
        download_URL_textbox.send_keys(download_URL)

    def __type_in_new_download_location(self, target_directory):
        choose_another_folder_link = self.__WebDriver.get_element_when_accessible(By.XPATH, "//a[contains(text(),'Choose another folder')]")
        choose_another_folder_link.click()
        sleep(1)
        choose_another_folder_textbox = self.__WebDriver.get_element_when_accessible(By.XPATH, "//div[4]/div/div/div/div/input")
        choose_another_folder_textbox.send_keys(target_directory.__str__())
        sleep(1)
        OK_button = self.__WebDriver.get_element_when_accessible(By.XPATH, "/html/body/div[4]/div/div/div/div/div[2]/div[1]/button[1]")
        OK_button.click()   
        sleep(1)
        continue_button = self.__WebDriver.get_element_when_accessible(By.XPATH, "/html/body/div[4]/div/div/div/div/div[1]/button[1]")
        continue_button.click()

    def __wait_until_download_is_added(self):
        for num_of_refreshes in range(10):
            try:
                expander_button = self.__WebDriver.get_element_when_accessible(By.CLASS_NAME, "expandButton")
                expander_button.click()
                return
            except:
                self.__WebDriver.refresh()
                continue
        
        raise Exception("Download is not added")


    def __start_download_for_current_item(self):
        sleep(1)
        actions_hyperlink = self.__WebDriver.get_element_when_accessible(By.XPATH, '//*[@id="gwtContent"]/div/div[1]/div[1]/div[2]/div[7]/a')
        actions_hyperlink.click()
        sleep(1)
        add_to_downloads_button = self.__WebDriver.get_element_when_accessible(By.XPATH, "/html/body/div[3]/div/div/a[1]")
        add_to_downloads_button.click()
        sleep(1)

    def __has_nfo_file(self, target_nfo_directory):
        for potential_nfo_file in os.listdir(target_nfo_directory):
            potential_nfo_file_as_str = potential_nfo_file.__str__()
            if potential_nfo_file_as_str.endswith("info"):
                nfo_file_directory = target_nfo_directory.__str__() + "\\" + potential_nfo_file_as_str
                os.remove(nfo_file_directory)
                return True
        return False

    def __print_status(self):
        if self.__error_log_dict:
            "Errors found!"
            print(self.__error_log_dict.keys)
        else :
             "Success!"
    
    def __check_for_error(self):
        sleep(2)
        try:
            error_status_elem = self.__WebDriver.get_element_when_accessible(By.XPATH, "//*[ contains (text(), ‘An Error’ ) ]")
        except:
            return
        else: 
            error_status_elem.click()
            ActionChains.context_click(error_status_elem)
            force_download_button = self.__WebDriver.get_element_when_accessible(By.XPATH, "/html/body/div[3]/div/div/a[4]/text()")
            force_download_button.click()
#------------------------------------------------------------------------------------------------------------------------------------------
#Driver 
video_downloader = Driver()

#1) Set download location here:
video_downloader.set_download_location(r"C:\Users\mihir\Documents\MIT\6.1900 Introduction to Low-level Programming in C and Assembly (F22B) [NEW]\Material\Weekly Material\Week 5")


#2) Add Panopto Video URL's here and name of parent folder
#video_downloader.add("TestParentFolder", "https://mit.hosted.panopto.com/Panopto/Pages/Viewer.aspx?id=d4e68f2a-038f-4846-b9ed-af4400d73902")
video_downloader.add("Lecture", "https://mit.hosted.panopto.com/Panopto/Pages/Viewer.aspx?id=66a1b2c7-acbe-4b87-b4cd-af0000e095d8")


video_downloader.start_downloads()
#------------------------------------------------------------------------------------------------------------------------------------------     
