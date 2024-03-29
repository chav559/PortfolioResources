# -*- coding: utf-8 -*-
"""Scraping_HTML.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Cf9pBZOEzMhG4iJJhPZjErfMBWO5jDVu
"""

from bs4 import BeautifulSoup
import requests
import sqlite3
import time
from tqdm import tqdm
from selenium import webdriver
from selenium.webdriver.common.keys import Keys 

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
from selenium import webdriver

import pickle

# options = webdriver.ChromeOptions()
# options.add_argument("--log-level=3") 
# driver = uc.Chrome(options=options)

# driver.get("https://www.google.com/search?q=hello&oq=hello&aqs=chrome.0.69i59.776j0j15&sourceid=chrome&ie=UTF-8")

# driver.close()



with open ("parking_URLs", "rb") as f:
    park_locL = pickle.load(f)

len(park_locL)



location_elementsD = {}

# gets blocked every 40 or so queries; need to rerun manually

for i, url in enumerate(park_locL):
    
    options = webdriver.ChromeOptions() 

    # this parameter tells Chrome that
    # it should be run without UI (Headless)
    options.headless = True

    driver = uc.Chrome(options=options)

    driver.get(url)  

    #     driver.maximize_window()
    time.sleep(3)

    # this is just to ensure that the page is loaded 

    # time.sleep(5)  
    # WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.CLASS_NAME, "cell")))

    html = driver.page_source 


    # this renders the JS code and stores all 
    # of the information in static HTML code. 


    # Now, we could simply apply bs4 to html variable 

    soup = BeautifulSoup(html, "html.parser") 
    driver.close()
    time.sleep(3)


    # creating attribute variables
    locationContent_elem = soup.find("div", {"class": "LocationDetails"})
    
    # checking if i got blocked
    type_spots = locationContent_elem.find(class_="LocationDetailsTitleBar__subTitle").get_text()
    # any find command would do the trick
    
    location_elementsD["location " + str(i)] = {"url":url, "element":locationContent_elem}
    
    print(i)
    if i%15 == 0:
        time.sleep(90)
    elif i%29 == 0:
        with open ("loc_elems_dict3", "wb") as f:
            pickle.dump(location_elementsD, f)
        time.sleep(360)
    elif i%39 == 0:
        time.sleep(240)

# location_elementsD



import sys
sys.setrecursionlimit(30000)

with open ("loc_elems_dict", "wb") as f:
    pickle.dump(location_elementsD, f)





