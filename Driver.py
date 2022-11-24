import PanoptoEndpointFinder as PEF
from collections import deque 
from selenium import webdriver as WD

class Driver: 
    '''Driver Class'''

    def __init__(self):
        self.__DownloadQueue = deque()
        self.__PanoptoEndpointFinder = PEF.PanoptoEndpointFinder()
        #self.__download_location = None

    def add(self, video_URL):
        #if self.download_location == None:
        #    raise Exception("Set download location first by calling set_download_location")

        self.__DownloadQueue.append(video_URL)
    
    def start_downloads(self):

        while self.__DownloadQueue:
            current_video_URL = self.__DownloadQueue.popleft()
            if "panopto.com" in current_video_URL:
                self.__handle_panopto_videos(current_video_URL)
            #__download(current_video_URL)
            

    def __handle_panopto_videos(self, panopto_video_URL):
        list_of_panopto_endpoint_URLs = self.__PanoptoEndpointFinder.get_URL_list(panopto_video_URL)
        
        while list_of_panopto_endpoint_URLs:
            self.__DownloadQueue.appendleft(list_of_panopto_endpoint_URLs.pop(0))
            
    
    #def set_download_location(self, download_location): 
    #    self.download_location = download_location
    #
    #    return 0


#------------------------------------------------------------------------------------------------------------------------------------------
#Driver 
video_downloader = Driver()

#1) Set download location here:
#Downloader.set_download_location("")


#2) Add Panopto Video URL's here and name of parent folder
video_downloader.add("https://mit.hosted.panopto.com/Panopto/Pages/Viewer.aspx?id=d4e68f2a-038f-4846-b9ed-af4400d73902")
video_downloader.add("https://mit.hosted.panopto.com/Panopto/Pages/Viewer.aspx?id=4acfcb21-72cc-4efd-be2c-af0000e0957e")

video_downloader.start_downloads()
#------------------------------------------------------------------------------------------------------------------------------------------     
