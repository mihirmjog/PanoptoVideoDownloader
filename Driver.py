import PanoptoEndpointFinder as PEF
from collections import deque
import pathlib
from selenium import webdriver as WD
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import *

class Driver: 
    '''Driver Class'''

    def __init__(self):
        self.__DownloadQueue = deque()        
        self.__PanoptoEndpointFinder = PEF.PanoptoEndpointFinder()
        self.__download_location = None
        self.WebDriver = None

    def set_download_location(self, download_location): 
        target_directory = pathlib.Path(pathlib.PureWindowsPath(download_location).as_posix())
        target_directory.mkdir(parents=True, exist_ok= True)
        download_location.join("/")
        self.__download_location = target_directory

    def add(self, video_URL, folder_name):
        if self.__download_location == None:
            raise Exception("Set Download Location first!")
        
        if folder_name is None: #TODO Remove if/else clause after finished 
            parent_folder = self.__download_location
        else:
            parent_folder= self.__download_location + folder_name

        download_item = (parent_folder, video_URL)
        self.__DownloadQueue.append(download_item)
    
    def start_downloads(self):

        while self.__DownloadQueue:
            current_download_item = self.__DownloadQueue.pop()
            (current_download_item_parent_folder, current_download_URL) = current_download_item
            
            if "panopto.com" in current_download_URL:
                self.__handle_panopto_videos(current_download_item_parent_folder, current_download_URL) #Reinserts download URL of every camera of a panopto video
            else:
                self.__download_current_item(current_download_item_parent_folder, current_download_URL)
            
        self.__PanoptoEndpointFinder.close_finder()
        #self.__close_downloader() 

    def __handle_panopto_videos(self, parent_folder, video_URL):
        list_of_panopto_endpoint_URLs = self.__PanoptoEndpointFinder.get_URL_list(video_URL)

        for panopto_endpoint_URL in list_of_panopto_endpoint_URLs:
            download_item = (parent_folder, panopto_endpoint_URL)
            self.__DownloadQueue.appendleft(download_item)

    def __download_current_item(self, parent_folder, download_URL):
    #    self.__get_initialized_WebDriver()
    #
        return

    #def __get_initialized_WebDriver(self):
    #    chrome_options = WD.ChromeOptions()
    #    chrome_options.add_argument("user-data-dir=C:/Users/mihir/AppData/Local/Google/Chrome/User Data") #Needed to enter MyJDownloader without entering login credentials
    #    chrome_options.add_argument("remote-debugging-port=9222")   
    #    self.WebDriver = WD.Chrome(options = chrome_options)

#------------------------------------------------------------------------------------------------------------------------------------------
#Driver 
video_downloader = Driver()

#1) Set download location here:
video_downloader.set_download_location(r"C:\Users\mihir\Documents\Test")


#2) Add Panopto Video URL's here and name of parent folder
video_downloader.add("https://mit.hosted.panopto.com/Panopto/Pages/Viewer.aspx?id=d4e68f2a-038f-4846-b9ed-af4400d73902", None)
video_downloader.add("https://mit.hosted.panopto.com/Panopto/Pages/Viewer.aspx?id=4acfcb21-72cc-4efd-be2c-af0000e0957e", None)

video_downloader.start_downloads()
#------------------------------------------------------------------------------------------------------------------------------------------     
