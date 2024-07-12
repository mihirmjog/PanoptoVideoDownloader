from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

capabalities = webdriver.DesiredCapabilities()
options = webdriver.ChromeOptions()
capabalities = webdriver.DesiredCapabilities
options.add_argument((r"C:\Users\mihir\AppData\Local\Google\Chrome\User Data\Profile 1"))
options.set_capability('goog:loggingPrefs', {
                                                'performance' : 'ALL',
                                                'level'       : 'ALL',})

options.add_experimental_option("perfLoggingPrefs", {
                                                "traceCategories" : "devtools.Network.requestWillBeSent"})
service = Service(r'C:\Users\mihir\Documents\Git\VideoDownloader\bin\chromedriver.exe')  # Update with your ChromeDriver path

driver = webdriver.Chrome(options= options, service= service)

driver.get('https://www.selenium.dev')
performance_logs = driver.get_log('performance')

for entry in performance_logs:
    print(entry)

print("Succesfully printed all logs!")
driver.quit()

options = webdriver.ChromeOptions()
capabalities = webdriver.DesiredCapabilities()

#configure the DesiredCapabilities() object

options.set_capability(capabalities)
driver = webdriver.Chrome(options= options, service= service)
