from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.chrome.options import Options
import pickle
import requests
from bs4 import BeautifulSoup
import time
import pandas as pd
import numpy as np


drv_path = "C:\\Users\\LENOVO\\Documents\\chromedriver\\chromedriver.exe"

chrome_options = Options()
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-gpu")
# chrome_options.add_argument("--headless")
driver = webdriver.Chrome(drv_path, options=chrome_options)
# driver.minimize_window()

url = 'https://glints.com/id/opportunities/jobs/explore?jobCategories=1'
# implicitly_wait tells the driver to wait before throwing an exception
driver.implicitly_wait(30)
# driver.get(url) opens the page
driver.get(url)
# This starts the scrolling by passing the driver and a timeout
scroll_pause_time = 2# You can set your own pause time. My laptop is a bit slow so I use 1 sec
screen_height = driver.execute_script("return window.screen.height;")   # get the screen height of the web
i = 1

while True:
    # scroll one screen height each time
    driver.execute_script("window.scrollTo(0, {screen_height}*{i});".format(screen_height=screen_height, i=i))  
    i += 1
    time.sleep(scroll_pause_time)
    # update scroll height each time after scrolled, as the scroll height can change after we scrolled the page
    scroll_height = driver.execute_script("return document.body.scrollHeight;")  
    # Break the loop when the height we need to scroll to is larger than the total scroll height
    if (screen_height) * i > scroll_height:
        break 
        

soup_a = BeautifulSoup(driver.page_source, 'lxml')
links = []
for loc in soup_a.find_all('a', {"class":"CompactOpportunityCardsc__CardAnchorWrapper-sc-1xtox99-17 PRbbx job-search-results_job-card_link"}):
       for a in soup_a.find_all('a', href=True): 
            links.append(a['href'])

df = pd.DataFrame(links)
loker=df[df[0].str.contains("/id/opportunities/", na=False)]
loker=loker.drop_duplicates(keep='last')
loker.to_csv('dat-21.csv',index=False)