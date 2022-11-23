import APIEndpointFinder as AEF
import queue 

class PanoptoVideoDownloader: 
    '''Driver Class'''

    def __init__(self): #TODO Determine what arguments are needed for initializer
        self.PanoptoVideoQueue = queue.Queue()
        self.EndpointURLFinder = AEF.APIEndpointFinder()
        #self.download_location = None


    def add(self, panopto_video_URL):
        #if self.download_location == None:
        #    raise Exception("Set download location first by calling set_download_location")

        self.PanoptoVideoQueue.put(panopto_video_URL)
        
    
    def start_downloads(self):
        APIEndpointsMap = {}

        while not self.PanoptoVideoQueue.empty():
            current_video_URL = self.PanoptoVideoQueue.get() 
            APIEndpointsMap[current_video_URL] = self.EndpointURLFinder.get_URL_list(current_video_URL)



    #def set_download_location(self, download_location): 
    #    self.download_location = download_location
    #
    #    return 0


#------------------------------------------------------------------------------------------------------------------------------------------
#Driver 
panapto_video_downloader = PanoptoVideoDownloader()

#1) Set download location here:
#Downloader.set_download_location("")


#2) Add Panopto Video URL's here
#TODO Change arguments given to downloader to specify location OR create a set_download_location as a function
panapto_video_downloader.add("https://mit.hosted.panopto.com/Panopto/Pages/Viewer.aspx?id=d4e68f2a-038f-4846-b9ed-af4400d73902")
panapto_video_downloader.add("https://mit.hosted.panopto.com/Panopto/Pages/Viewer.aspx?id=4acfcb21-72cc-4efd-be2c-af0000e0957e")

panapto_video_downloader.start_downloads()
#------------------------------------------------------------------------------------------------------------------------------------------     
