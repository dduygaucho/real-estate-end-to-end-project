import re
from json import dump
from collections import defaultdict
# user packages
import time
import json
from bs4 import BeautifulSoup
import requests
import numpy as np
import pandas as pd

# pylint: disable=E1101

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.4 Safari/605.1.15'
session = requests.Session()
session.headers.update({'User-Agent': USER_AGENT})

BASE_URL = "https://www.domain.com.au"

# begin code
url_links = []
property_metadata = defaultdict(dict)

# generate list of urls to visit
# all vic postcodes are in 3000->3999
# iterating through all domain rental pages for all vic postcodes
for postcode in range(3000,4000):
    first_page_url = f"https://www.domain.com.au/rent/?ssubs=0&postcode={postcode}&page=1"
    bs_object = BeautifulSoup(session.get(first_page_url).text, 'lxml')

    # finding the number of properties listed for rent on domain in that postcode 
    num_properties_line = re.findall(r'[0-9]+ Rental Properties in postcode', bs_object.text)
    # if no properties for rent in that postcode skip to next
    if(len(num_properties_line) == 0):
        continue
    num_properties = int(re.findall(r'[0-9]+', num_properties_line[0])[0])
    # since there is a maximum of 20 properties on each page, num properties // 20 == the number of pages 
    npages = int(np.ceil(num_properties/20))

    # iterating through each page and finding all listing urls 
    for page in range(1, npages + 1):
        url = BASE_URL + f"/rent/?ssubs=0&postcode={postcode}&page={page}"
        print(f"Visiting {url}")
        bs_object = BeautifulSoup(session.get(url).text, 'lxml')

        # find the unordered list (ul) elements which are the results, then
        # find all href (a) tags that are from the base_url website.
        index_links = bs_object \
            .find(
                "ul",
                {"data-testid": "results"}
            ) \
            .findAll(
                "a",
                href=re.compile(f"{BASE_URL}/*") # the `*` denotes wildcard any
            )

        for link in index_links:
            # if its a property address, add it to the list
            if 'address' in link['class']:
                url_links.append(link['href'])
# list of urls saved in json file 
with open('../data/landing/property_urls.json', 'w') as f:
    dump(url_links, f)

options = webdriver.ChromeOptions()
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--no-sandbox")
driver = webdriver.Chrome(options=options)
driver.implicitly_wait(5)

url_links = pd.read_json("../data/landing/property_urls.json")[0]
property_metadata = defaultdict(dict)

# for each url in list we recoord all relevant information
for property_url in url_links:
    driver.get(property_url)
    driver.maximize_window()
    # sometimes the 'read more' button in the description is not there or takes a few seconds to appear
    # if after 5 seconds, the web driver cannot find the button, assume the button is not there (short or no description)
    # if button is found, scroll down and click it 
    try:
        WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, "//button[contains(text(),'Read more')]")))
        button = driver.find_element("xpath", "//button[contains(text(),'Read more')]")
        driver.execute_script("arguments[0].scrollIntoView();", button)
        driver.execute_script("arguments[0].click();", button) 
    except TimeoutException:
        print("no read more button ")

    bs_object=BeautifulSoup(driver.page_source, "lxml")
    # sometimes urls led to listings for properties that weren't for rent (maybe already leased or for sale instead)
    # in this case, skip to next listing 
    for_rent = bs_object.find("a", {"href":"/rent/", "alt":"Rent", "class":"css-ou12a4"})
    if for_rent is None:
        print("not for rent")
        continue
    

    try: 
        # looks for the header class to get property name
        property_metadata[property_url]['name'] = bs_object \
            .find("h1", {"class": "css-164r41r"}) \
            .text

        # looks for the div containing a summary title for cost
        property_metadata[property_url]['cost_text'] = bs_object \
            .find("div", {"data-testid": "listing-details__summary-title"}) \
            .text

        # extract coordinates from the hyperlink provided
        # i'll let you figure out what this does :P
        property_metadata[property_url]['coordinates'] = [
            float(coord) for coord in re.findall(
                r'destination=([-\s,\d\.]+)', # use regex101.com here if you need to
                bs_object \
                    .find(
                        "a",
                        {"target": "_blank", 'rel': "noopener noreferrer"}
                    ) \
                    .attrs['href']
            )[0].split(',')
        ]

        # get rooms and parking
        rooms = bs_object \
                .find("div", {"data-testid": "property-features"}) \
                .findAll("span", {"data-testid": "property-features-text-container"})

        # rooms
        property_metadata[property_url]['rooms'] = [
            re.findall(r'\d+\s[A-Za-z]+', feature.text)[0] for feature in rooms
            if 'Bed' in feature.text or 'Bath' in feature.text
        ]

        # parking
        property_metadata[property_url]['parking'] = [
            re.findall(r'\S+\s[A-Za-z]+', feature.text)[0] for feature in rooms
            if 'Parking' in feature.text
        ]

        # reading full description 
        desc = bs_object \
            .find("div", {"name":"listing-details__description", "data-testid":"listing-details__description","class":'css-bq4jj8'})\
            .find_all("p", recursive=True)
        
        # getting property type (usually located in same area as description)
        comb_desc = ""
        for i in desc:
            line = i.text
            if line[0:14] != "Property type:":
                comb_desc = comb_desc + line
            else:
                property_metadata[property_url]['property_type'] = line[15:]

        property_metadata[property_url]['desc'] = comb_desc
        
        # getting additional features 
        property_features = bs_object.find_all("li", {"data-testid":"listing-details__additional-features-listing",\
                                                      "class":"css-vajaaq"})
        features_list = []
        for feature in property_features:
            features_list.append(feature.text)
        property_metadata[property_url]['property_features'] = features_list

        # finding internal and land area
        internal_area = bs_object \
            .select_one('li:-soup-contains("Internal area")')
            #.strong.find_all('span', recursive=False)[0]
        if (internal_area != None):
            property_metadata[property_url]['internal_area'] = [
            re.findall(r'[0-9]+', internal_area.text)[0]
            ]        
        land_area= bs_object \
                .select_one('li:-soup-contains("Land area")')
        if (land_area != None):
            property_metadata[property_url]['land_area'] = [
            re.findall(r'[0-9]+', land_area.text)[0]
            ]        



    except AttributeError:
        print(f"Issue with {property_url}, see raw dump below")
        #print(bs_object.text)
        continue

with open('../data/landing/domain_scraped_data.json', 'w') as f:
    dump(property_metadata, f)

# saving scraped data as csv 
domain_data = pd.read_json("../data/landing/domain_scraped_data.json").transpose()
domain_data.to_csv("../data/landing/domain_scraped_data.csv")
