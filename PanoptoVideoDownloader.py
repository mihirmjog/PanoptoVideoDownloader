import APIEndpointFinder as AEF
import queue 

class PanoptoVideoDownloader: 
    '''Driver Class'''

    def __init__(self): #TODO Determine what arguments are needed for initializer
        self.PanoptoVideoQueue = queue.Queue()
        self.EndpointURLFinder = AEF.APIEndpointFinder()

    def start_downloads(self):
        APIEndpointsMap = {}

        while not self.PanoptoVideoQueue.empty():
            current_video_URL = self.PanoptoVideoQueue.get() 
            APIEndpointsMap[current_video_URL] = self.EndpointURLFinder.get_URL_list(current_video_URL)

        return 

    def add(self, panopto_video_URL):
        self.PanoptoVideoQueue.put(panopto_video_URL)
        
        return 
    
#----------------------------------------------------------------------------------------------------------
#Driver 
Downloader = PanoptoVideoDownloader()

#Add Panopto Video URL's here
#TODO Change arguments given to downloader to specify location, potentially including overriden methods for maximum flexibility
Downloader.add("https://mit.hosted.panopto.com/Panopto/Pages/Viewer.aspx?id=d4e68f2a-038f-4846-b9ed-af4400d73902")
Downloader.add("https://mit.hosted.panopto.com/Panopto/Pages/Viewer.aspx?id=4acfcb21-72cc-4efd-be2c-af0000e0957e")

Downloader.start_downloads()
#----------------------------------------------------------------------------------------------------------     
