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

        relative_folder_directory = "/" + folder_name
        download_directory = self.__append_to_filepath(self.__download_location, relative_folder_directory)
        self.__create_directory(download_directory)

        download_item = (download_directory, video_URL)
        self.__DownloadQueue.put(download_item)
    
    def start_downloads(self):
        while self.__DownloadQueue:
            current_download_item = self.__DownloadQueue.get()
            (download_dir_for_current_item, current_download_URL) = current_download_item
            if "panopto.com" in current_download_URL:
                try:
                    PanoptoEndpointFinder = PEF.PanoptoEndpointFinder()
                    list_of_panopto_endpoints = PanoptoEndpointFinder.get_URL_list(current_download_URL)
                #except Exception as exception_message:
                #    self.__error_log_dict[current_download_URL] = exception_message #TODO Add actual error messages as value
                else:
                    for panopto_endpoint in list_of_panopto_endpoints:
                        self.__download_current_item(download_dir_for_current_item, panopto_endpoint)
            else:
                self.__download_current_item(download_dir_for_current_item, current_download_URL)
        self.__print_status()

    def __create_directory(self, target_directory):
        target_directory.mkdir(parents=True, exist_ok= True)

    def __download_current_item(self, download_dir, download_URL):
        try:
            #TODO Check if sleep functions are necessary
            WebDriver = Configured_WD.ConfiguredWD(logging = False)
            WebDriver.get("https://my.jdownloader.org")
            self.__go_to_my_JDownloader(WebDriver)
            self.__click_on_add_new_link(WebDriver)
            self.__type_in_download_URL(WebDriver, download_URL)
            self.__type_in_new_download_location(WebDriver, download_dir)
            self.__wait_until_download_is_added(WebDriver)
            self.__start_download_for_current_item(WebDriver)
            while not self.__has_info_file(download_dir): #JDownloader creates an "info" file after download finishes.
                sleep(0.5)                                #Once the info file is detected, __has_info_file() removes
                continue                                  #it before exitng the while loop.
            WebDriver.quit()
        except Exception as exception_message:
                self.__error_log_dict[download_URL] = exception_message #TODO Add actual error messages as value
        return

    def __append_to_filepath(self, original_filepath, path_to_append_as_str):
        original_filepath_as_str = original_filepath.__str__()
        new_filepath_as_string = original_filepath_as_str + path_to_append_as_str
        new_filepath = pathlib.Path(pathlib.PureWindowsPath(new_filepath_as_string).as_posix())

        return new_filepath
        
    def __go_to_my_JDownloader(self, WebDriver):
        my_jdownloader_button = WebDriver.get_element_when_accessible(By.XPATH, "/html/body/div[1]/div[2]/div/div/div[2]/div[1]/div[2]/div/div/div/img")
        my_jdownloader_button.click()

    def __click_on_add_new_link(self, WebDriver):
        current_URL = WebDriver.current_url
        link_collector_URL = current_URL.replace(":downloads", ":links")
        WebDriver.get(link_collector_URL)
        WebDriver.refresh()
        add_links_button = WebDriver.get_element_when_accessible(By.XPATH, "//*[contains(text(),'Add links')]")
        add_links_button.click()
        sleep(1)

    def __type_in_download_URL(self, WebDriver, download_URL):
        download_URL_textbox = WebDriver.get_element_when_accessible(By.XPATH, "/html/body/div[4]/div/div/div/div/table/tbody/tr[1]/td[2]/div[1]/textarea")
        download_URL_textbox.send_keys(download_URL)

    def __type_in_new_download_location(self, WebDriver, target_directory):
        choose_another_folder_link = WebDriver.get_element_when_accessible(By.XPATH, "//a[contains(text(),'Choose another folder')]")
        choose_another_folder_link.click()
        sleep(1)
        choose_another_folder_textbox = WebDriver.get_element_when_accessible(By.XPATH, "//div[4]/div/div/div/div/input")
        choose_another_folder_textbox.send_keys(target_directory.__str__())
        sleep(1)
        OK_button = WebDriver.get_element_when_accessible(By.XPATH, "/html/body/div[4]/div/div/div/div/div[2]/div[1]/button[1]")
        OK_button.click()   
        sleep(1)
        continue_button = WebDriver.get_element_when_accessible(By.XPATH, "/html/body/div[4]/div/div/div/div/div[1]/button[1]")
        continue_button.click()

    def __wait_until_download_is_added(self, WebDriver): 
        for num_of_refreshes in range(10):               
            try:
                package_expander_button = WebDriver.get_element_when_accessible(By.CLASS_NAME, "expandButton")
                package_expander_button.click()
                return
            except:
                WebDriver.refresh()
                continue
        
        raise Exception("Download is not added")

    def __start_download_for_current_item(self, WebDriver):
        sleep(1)
        actions_hyperlink = WebDriver.get_element_when_accessible(By.XPATH, '//*[@id="gwtContent"]/div/div[1]/div[1]/div[2]/div[7]/a')
        actions_hyperlink.click()
        sleep(1)
        add_to_downloads_button = WebDriver.get_element_when_accessible(By.XPATH, "/html/body/div[3]/div/div/a[1]")
        add_to_downloads_button.click()
        sleep(1)

    def __has_info_file(self, target_nfo_directory):
        for potential_info_file in os.listdir(target_nfo_directory):
            potential_info_file_as_str = potential_info_file.__str__()
            if potential_info_file_as_str.endswith("info"):
                sleep(1)
                info_file_directory = target_nfo_directory.__str__() + "\\" + potential_info_file_as_str #Avoids use of __apend_filepath() which
                os.remove(info_file_directory)                                                           #returns pathlib object instead of string
                return True
            else:
                sleep(0.5)
        return False

    def __print_status(self):
        if self.__error_log_dict:
            "Errors found!"
            print(self.__error_log_dict.keys)
        else :
             "Success!"

#------------------------------------------------------------------------------------------------------------------------------------------
#Driver 
video_downloader = Driver()

#1) Set download location here:
video_downloader.set_download_location(r"D:\MIT\6.5620[J] Cryptography and Cryptanalysis (F22) [6.857]\Lecture Videos")

#2) Add Panopto Video URL's here and name of parent folder
video_downloader.add("Lecture 4", "https://mit.hosted.panopto.com/Panopto/Pages/Embed.aspx?id=addc5a32-fbca-4680-94dc-af0c00d7840f")
video_downloader.add("Lecture 5", "https://mit.hosted.panopto.com/Panopto/Pages/Viewer.aspx?id=ecce115e-11c5-4999-8516-af1300d72e1a")
video_downloader.add("Lecture 6", "https://mit.hosted.panopto.com/Panopto/Pages/Viewer.aspx?id=12594d13-467f-4d4f-834d-af1a00d725f7")
video_downloader.add("Lecture 7", "https://mit.hosted.panopto.com/Panopto/Pages/Embed.aspx?id=734f395a-bd5e-459e-af7b-af1a00d7b38b")
video_downloader.add("Lecture 8", "https://mit.hosted.panopto.com/Panopto/Pages/Embed.aspx?id=0163f5ee-e1f6-4606-ac87-af2100d69d7e")
video_downloader.add("Lecture 9", "https://mit.hosted.panopto.com/Panopto/Pages/Embed.aspx?id=bd6c4da3-13e2-4132-a33c-af2100d6d9fa")
video_downloader.add("Lecture 10", "https://mit.hosted.panopto.com/Panopto/Pages/Viewer.aspx?id=1a061ba5-a322-41f6-887e-af2800d69ca4")
video_downloader.add("Lecture 11", "https://mit.hosted.panopto.com/Panopto/Pages/Viewer.aspx?id=9fe277ca-d710-4129-a374-af2f00d698ed")
video_downloader.add("Lecture 12", "https://mit.hosted.panopto.com/Panopto/Pages/Viewer.aspx?id=f34cdd78-615d-4fdb-8211-af2f00d71262")
video_downloader.add("Lecture 13", "https://mit.hosted.panopto.com/Panopto/Pages/Viewer.aspx?id=d752b1a9-ff56-43c1-b875-af3600d69162")
video_downloader.add("Lecture 14", "https://mit.hosted.panopto.com/Panopto/Pages/Viewer.aspx?id=29fe2eb9-ce2a-43ee-99be-af3600d6d190")
video_downloader.add("Lecture 15", "https://mit.hosted.panopto.com/Panopto/Pages/Viewer.aspx?id=c2b9e102-a93c-49c9-80dc-af3d00d6a398")
video_downloader.add("Lecture 16", "https://mit.hosted.panopto.com/Panopto/Pages/Viewer.aspx?id=92af7010-f885-4af2-b0f6-af3d00d71afd")
video_downloader.add("Lecture 17", "https://mit.hosted.panopto.com/Panopto/Pages/Viewer.aspx?id=49b56d96-fa8c-4b14-b9da-af4400d69d3a&fbclid=IwAR2VXhDQAzGWZVCuozWCSgV1FKglGz0QDR9dk6VEBBdygRPRUUE7Ru2BLuU")
#LECTURE 18 ALREADY ARCHIVED
video_downloader.add("Lecture 19", "https://mit.zoom.us/rec/share/j5otCaGTJf5z0uhhqRHL04DIxKYaFvGALIBlYVBedFDvlca9z63k8bKSJXHvuQMU.uQY3_jD528DItTNK")
video_downloader.add("Lecture 20", "https://mit.hosted.panopto.com/Panopto/Pages/Viewer.aspx?id=7c4bdf51-d534-4989-8438-af4b00d73102")
video_downloader.add("Lecture 21", "https://mit.hosted.panopto.com/Panopto/Pages/Viewer.aspx?id=809ed765-b238-41cf-b0be-af5300669485")
video_downloader.add("Lecture 22", "https://mit.hosted.panopto.com/Panopto/Pages/Viewer.aspx?id=359fc140-03f2-4e9a-81c9-af5900d6aeff")
video_downloader.add("Lecture 23", "https://mit.hosted.panopto.com/Panopto/Pages/Viewer.aspx?id=172d2a9a-eb3d-424d-afeb-af5900d70d90&fbclid=IwAR3sRfoTgL51p5G0uHnptBvcml15li_ZLXh2S08vinNA-4EGEchRpJx2QyU")
video_downloader.add("Lecture 24", "https://mit.hosted.panopto.com/Panopto/Pages/Viewer.aspx?id=93254a33-215a-44bf-9225-af6000d6c3c7")
video_downloader.add("Lecture 25", "https://mit.hosted.panopto.com/Panopto/Pages/Viewer.aspx?id=47b1595d-d24c-47cf-b4bc-af6000d71fcf")


#3) Start downloads
video_downloader.start_downloads()


#------------------------------------------------------------------------------------------------------------------------------------------     
