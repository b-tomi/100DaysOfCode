# Zillow Rental Research

import time

import requests
from bs4 import BeautifulSoup
from selenium import webdriver

# Note: expects Google Chrome and the appropriate ChromeDriver to be properly installed on the system
# https://chromedriver.chromium.org/downloads

ZILLOW_URL = "https://www.zillow.com"
# separate base url, to handle multiple pages
SEARCH_BASE = "https://www.zillow.com/san-francisco-ca/rentals/"
# rest of the url with the required parameters set
SEARCH_REST = "1-_beds/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22usersSearchTerm%22%3A%22San%20Francisco%2" \
              "C%20CA%22%2C%22mapBounds%22%3A%7B%22west%22%3A-122.61529005957031%2C%22east%22%3A-122.25136794042969%" \
              "2C%22south%22%3A37.561687998797254%2C%22north%22%3A37.988279538758576%7D%2C%22regionSelection%22%3A%5" \
              "B%7B%22regionId%22%3A20330%2C%22regionType%22%3A6%7D%5D%2C%22isMapVisible%22%3Atrue%2C%22filterState%" \
              "22%3A%7B%22fsba%22%3A%7B%22value%22%3Afalse%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A" \
              "%7B%22value%22%3Afalse%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afa" \
              "lse%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22pmf%22%3A%7B%22value%22%3Afalse%7D%2C%22pf%22%3A%" \
              "7B%22value%22%3Afalse%7D%2C%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22ah%22%3A%7B%22value%22%3Atrue%7D%" \
              "2C%22mp%22%3A%7B%22max%22%3A3000%7D%2C%22price%22%3A%7B%22max%22%3A911817%7D%2C%22beds%22%3A%7B%22min" \
              "%22%3A1%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A11%7D"
# understandably, the form is no longer accepting entries
FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLScW44f__acDrRrwD7EymVLGHBALUf31OgZehn80k_zpH2rAVg/viewform"


def get_listings(page):
    """Reads listings on a page and returns them as a LIST."""
    # after the initial page, the url changes
    if page == 1:
        url = SEARCH_BASE + SEARCH_REST
    else:
        url = f"{SEARCH_BASE}{page}_p/{SEARCH_REST}"
    # pretend to be a web browser to avoid captcha
    headers = {
        "Accept-Language": "en-US,en;q=0.9,ja-JP;q=0.8,ja;q=0.7",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/87.0.4280.141 Safari/537.36 "
    }
    response = requests.get(url=url, headers=headers)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    # get a list of listings on the page
    listings = soup.select(".list-card-info")
    result_list = []

    # extract the useful data for each listing
    for listing in listings:
        url = listing.select_one(".list-card-link").get("href")
        address = listing.select_one(".list-card-addr").get_text()
        price = listing.select_one(".list-card-price").get_text()
        result_list.append({
            "address": address,
            "price": price,
            "url": url
        })
    return result_list


def enter_details(entry):
    """Takes details of a single listing as a DICT and enters them through the form."""
    driver.get(url=FORM_URL)
    time.sleep(2)
    # fix partial urls, using a ternary operator for practice
    url = entry["url"] if entry["url"][:4] == "http" else ZILLOW_URL + entry["url"]
    # fill out the fields
    driver.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/'
                                 'div[1]/input').send_keys(entry["address"])
    driver.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/'
                                 'div[1]/input').send_keys(entry["price"])
    driver.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/'
                                 'div[1]/input').send_keys(url)
    time.sleep(1)
    # submit the entry
    driver.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div/div').click()


rentals = []
# get listings from multiple pages, limiting the number to avoid processing 1400+ (as of right now) listings
# however, it should work for any number of pages, as long as it starts from 1 (i.e. not zero)
for num in range(1, 4):
    rentals += get_listings(page=num)

driver = webdriver.Chrome()
# enter the listings through the form, one at a time
for rental in rentals:
    enter_details(rental)
    time.sleep(1)

# close the browser window
driver.close()
