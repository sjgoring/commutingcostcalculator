# -*- coding: utf-8 -*-
"""
Created on Sun Nov 20 04:04:26 2022

@author: samgo
"""

import requests
from bs4 import BeautifulSoup as soup
import statistics

# Rental price scraper

def rental_price_scraper(location, radius, beds):
    
    #address = "https://www.zoopla.co.uk/to-rent/property/"+ postcode + "/?price_frequency=per_month&search_source=refine&radius=" + str(radius) + "&view_type=list&beds_max=" + str(beds)+"&beds_min=" +str(beds)
    address = "https://www.rightmove.co.uk/property-to-rent/find.html?searchType=RENT&locationIdentifier="+location+"&insId=1&radius="+str(radius)+"&sortType=1&minPrice=&maxPrice=&minBedrooms="+str(beds)+"&maxBedrooms="+str(beds)+"&displayPropertyType=&maxDaysSinceAdded=&sortByPriceDescending=&_includeLetAgreed=on&primaryDisplayPropertyType=&secondaryDisplayPropertyType=&oldDisplayPropertyType=&oldPrimaryDisplayPropertyType=&letType=&letFurnishType=&houseFlatShare="
    
    r = requests.get(address)
    s = soup(r.content, "html.parser")
    
    properties = s.find_all("div", class_="l-searchResult is-list")
        
    number_of_listings = s.find(
        "span", {"class": "searchHeader-resultCount"}
    )
    number_of_listings = number_of_listings.get_text()
    number_of_listings = int(number_of_listings.replace(",", ""))
    
    all_price = []
    
    #index=0
    
    for i in range(len(properties)):
    
        # tracks which apartment we are on in the page
        property_no = properties[i]
    
        # append price
        price = (
            property_no.find("span", class_="propertyCard-priceValue")
            .get_text()
            .strip()
        )
        all_price.append(price)
        
        # # Code to count how many listings we have scrapped already.
        # index = index + 24
    
        # if index >= number_of_listings:
        #     # break
    
    prices_pence = []
    for p in all_price:
        a, _ = p.split(" ")
        if ',' in a:
            a1, a2 = a.split(",")
            a = a1 + a2
        prices_pence.append(100*(int(a[1:len(a)])))
    return prices_pence


# Definitions
location = "STATION%5E6890"
radius = 1.0 #miles
beds = 2

ps = rental_price_scraper(location, radius, beds)

print(statistics.median(ps))
