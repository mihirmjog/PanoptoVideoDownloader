import PanoptoEndpointFinder as PEF
import queue
import pathlib
from selenium.webdriver.common.by import By
from selenium.common.exceptions import *
import psutil #TODO See if individual methods can be imported instead
import subprocess
import ConfiguredWD as Configured_WD
#TODO Determine what Seleniun dependencies should be deleted

class Driver: 
    '''Driver Class'''

    def __init__(self):
        self.__start_JDownloader()
        self.__DownloadQueue = queue.Queue()        
        self.__PanoptoEndpointFinder = PEF.PanoptoEndpointFinder()
        self.__download_location = None

        subprocess.Popen(['C:\Program Files\JDownloader\JDownloader\JDownloader2.exe'], stdout=subprocess.PIPE)

    def set_download_location(self, download_location): 
        target_directory = pathlib.Path(pathlib.PureWindowsPath(download_location).as_posix())
        self.__create_directory(target_directory)
        target_directory = self.__append_to_filepath(target_directory, "/") #TODO Place slash before folder_name
        self.__download_location = target_directory


    def add(self, folder_name, video_URL):
        if self.__download_location == None:
            raise Exception("Set Download Location first!")

        relative_folder_name = "/" + folder_name
        download_folder = self.__append_to_filepath(self.__download_location, relative_folder_name)
        self.__create_directory(download_folder)

        if "panopto.com" in video_URL:
            list_of_panopto_endpoints = self.__PanoptoEndpointFinder.get_URL_list(video_URL)
            for panopto_endpoint in list_of_panopto_endpoints:
                download_item = (download_folder, panopto_endpoint)
                self.__DownloadQueue.put(download_item)
        else:
            download_item = (download_folder, video_URL)
            self.__DownloadQueue.put(download_item)
    
    def start_downloads(self):
        self.__PanoptoEndpointFinder.close_finder()
        self.__WebDriver = Configured_WD.ConfiguredWD(logging = False)
        self.__WebDriver.get("https://my.jdownloader.org")
        self.__go_to_my_JDownloader()
        
        while self.__DownloadQueue:
            current_download_item = self.__DownloadQueue.get()
            (download_folder_for_current_item, current_download_URL) = current_download_item
            self.__download_current_item(download_folder_for_current_item, current_download_URL)
    
        self.__WebDriver.close()
    
    def __create_directory(self, target_directory):
        target_directory.mkdir(parents=True, exist_ok= True)

    def __start_JDownloader(self):
        for running_process in psutil.process_iter(attrs = ['name']):
            if running_process is "JDownloader2.exe":
                return

    def __download_current_item(self, download_folder_for_current_item, download_URL):
        self.__click_on_add_new_link()
        self.__type_in_download_URL(download_URL)
        self.__type_in_new_download_location(download_folder_for_current_item)
        self.__start_download_for_current_item()
        self.__wait_till_download_is_finished()
        #TODO Determine how program will know when download is finished
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
        add_links_button = self.__WebDriver.get_element_when_accessible(By.XPATH, "//a[contains(text(),'Add links')]")
        add_links_button.click()

    def __type_in_download_URL(self, download_URL):
        add_links_textbox = self.__WebDriver.get_element_when_accessible(By.XPATH, "/html/body/div[4]/div/div/div/div/table/tbody/tr[1]/td[2]/div[1]/textarea")
        add_links_textbox.send_keys(download_URL)
    
    def __type_in_new_download_location(self, target_directory):
        choose_another_folder_link = self.__WebDriver.get_element_when_accessible(By.XPATH, "//a[contains(text(),'Choose another folder')]")
        choose_another_folder_link.click()
        choose_another_folder_textbox = self.__WebDriver.get_element_when_accessible(By.XPATH, "//div[4]/div/div/div/div/input")
        choose_another_folder_textbox.send_keys(target_directory.__str__())
        OK_button = self.__WebDriver.get_element_when_accessible(By.XPATH, "/html/body/div[4]/div/div/div/div/div[2]/div[1]/button[1]")
        OK_button.click()

    def __start_download_for_current_item(self):
        continue_button = self.__WebDriver.get_element_when_accessible(By.XPATH, "/html/body/div[4]/div/div/div/div/div[1]/button[1]")
        continue_button.click()
        #TODO Click Play button

    def __wait_till_download_is_finished(self):
        return

#------------------------------------------------------------------------------------------------------------------------------------------
#Driver 
video_downloader = Driver()

#1) Set download location here:
video_downloader.set_download_location(r"C:\Users\mihir\Documents\Test")


#2) Add Panopto Video URL's here and name of parent folder
#video_downloader.add("TestParentFolder", "https://mit.hosted.panopto.com/Panopto/Pages/Viewer.aspx?id=d4e68f2a-038f-4846-b9ed-af4400d73902")
#video_downloader.add("TestParentFolder2", "https://mit.hosted.panopto.com/Panopto/Pages/Viewer.aspx?id=4acfcb21-72cc-4efd-be2c-af0000e0957e")
video_downloader.add("TestParentFolder3", "https://www.youtube.com/watch?v=FQS-i8TTUZs")
video_downloader.add("TestParentFolder3", "https://www.youtube.com/watch?v=esQyYGezS7c")

video_downloader.start_downloads()
#------------------------------------------------------------------------------------------------------------------------------------------     
