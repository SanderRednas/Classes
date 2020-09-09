# Run pip install selenium
# Run pip install selenium-requests
# Run pip install brotli
# Download chromedriver here: https://sites.google.com/a/chromium.org/chromedriver/downloads

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

from seleniumrequests import Chrome
import brotli
import json
import pandas as pd

user = "gahringbrian@gmail.com"
pwd = "test123"


# See https://stackoverflow.com/questions/53039551/selenium-webdriver-modifying-navigator-webdriver-flag-to-prevent-selenium-detec/53040904#53040904
# This is to prevent selenium detection
options = webdriver.ChromeOptions()
options.add_argument("start-maximized")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument("--disable-blink-features")
options.add_argument("--disable-blink-features=AutomationControlled")

driver = Chrome(options=options, executable_path=r'C:\Python\chromedriver.exe')
driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
driver.execute_cdp_cmd('Network.setUserAgentOverride', {
    "userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.53 Safari/537.36'})
#print(driver.execute_script("return navigator.userAgent;"))



# Login to the website
browser = driver.get("https://www.etoro.com/login")
print("Logging in...")
elem = driver.find_element_by_id("username")
elem.send_keys(user)
elem = driver.find_element_by_id("password")
elem.send_keys(pwd)
elem.send_keys(Keys.RETURN)

# While logged in send the GET request
response = driver.request('GET', 'https://www.etoro.com/sapi/trade-data-real/history/public/credit/flat?CID=5226327&ItemsPerPage=300&PageNumber=1&StartTime=2020-08-09T22:00:00.000Z&client_request_id=075f9f36-1413-46f2-841f-901dd396d85c')

# Convert to string
decompressed_response_str = str(response.content)

# Extract the position string
start = "nvar model = "
end = r",\r\n    txt = $$(\'TEXTAREA\')"
decompressed_response_str_extract = decompressed_response_str[decompressed_response_str.find(start)+len(start):decompressed_response_str.rfind(end)]

# Dump strimg into json
decompressed_response_str_extract_json = json.loads(decompressed_response_str_extract)

# Extract the positions from json
positions = decompressed_response_str_extract_json['PublicHistoryPositions']

# Put in dataframe
df = pd.DataFrame(positions)
df.to_csv("positions.csv")


# Close the connection
driver.close()





