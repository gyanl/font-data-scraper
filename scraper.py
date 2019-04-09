# Given a myfonts URL, extract all the tags.

from bs4 import BeautifulSoup
import pandas
import requests as r
import re

import random
import time
import os

list_of_fonts = []

list_names = []
list_creators = []
list_prices = []
list_styles = []

DUMP_FILE_NAME = 'fonts.csv'

START_URL = "https://www.myfonts.com/search/release_date%3A%5B%2A+TO+2020-12-31T23%3A59%3A59.000Z%5D/fonts/"


def init():
    response = r.get(START_URL)
    scrape_and_save(response, mode = 'w')


# append to existing excel sheet by default
# provide mode = 'w' if you want to overwrite
# existing excel sheet
def save_to_csv(mode="a"):
    global list_of_fonts, list_names, list_creators, list_prices, list_styles, DUMP_FILE_NAME
    df = pandas.DataFrame(
        data={
            "Font Name": list_names,
            "Foundry/Creator": list_creators,
            "Price": list_prices,
            "Styles": list_styles,
        }
    )
    header = False if mode is 'a' else True
    df.to_csv(DUMP_FILE_NAME, sep=",", mode=mode, index=False, header = header)
    print("Saved new sucessfully!")


def scrape_and_save(response, mode = 'a'):

    global list_of_fonts, list_names, list_creators, list_prices, list_styles

    html_soup = BeautifulSoup(response.text, "html.parser")
    # type(html_soup)

    font_containers = html_soup.find_all("div", class_="search-result-item")
    print(len(font_containers))

    i = 0

    for container in font_containers:
        i += 1
        # Code for Font name
        # for link in html_soup('h4'):
        name = container.h4.a.text
        list_names.append(name)
        # print(link.a.text, end=", ")

        # Code for Font Foundry/Creator
        # for link in html_soup('div', class_ = 'long-description'):
        creator = container.find("div", class_="long-description").a.text
        list_creators.append(creator)
        # print(link.a.text, end=", ")

        # Code for Price
        # for link in html_soup('span', class_ = 'regular-price'):
        price = container.find("span", class_="regular-price").text
        list_prices.append(price)
        # print(link.a.text, end=", ")

        # Code for Number of Styles
        # for link in html_soup():
        style = int(
            re.search(r"\d+", container.find("span", class_="description").text).group()
        )
        list_styles.append(style)
        # print(link.text, end=", ")

        print(i, end=" ")

    print("Done!")
    save_to_csv(mode = mode)

    # reset all the lists after sucessful save
    list_of_fonts = list_names = list_creators = list_prices = list_styles = []


# *****************************************************
# see if these are useful for scraping at larger volume

# read the existing csv file to create a set of fonts
# which have already been scraped.
# can help in making the scraping more efficient
def building_existing_scraped_set():
    pass


# is the given font already been scraped?
def has_already_been_scraped():
    return False
# *****************************************************


# next set of rows in from the search page network call
# keep a sane number for the range value: say 50 for each function call
def fetch_and_save_next_result_set(start_page, end_page):

    SEARCH_RESULTS_URL = (
        "https://www.myfonts.com/widgets/searchresults/searchresults.php"
    )
    headers = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "en-US,en;q=0.9",
        "content-length": "228",
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        "cookie": "__cfduid=d5f76bc1ec8f18f70c2b419634f5b9bbc1551972715; mf_new=1; mfclienthost=10.0.11.60;mfcart_live=794ee4537db845cf6ebf09b5089a6370b9744e41b68df81463a408151766; recentlyViewedFamilyIds=133793; mf_favbust=0; mf_followbust=0; apisession=451f01103fee461ef2a32676a79d89e9",
        "origin": "https://www.myfonts.com",
        "referer": "https://www.myfonts.com/search/release_date:[*+TO+2020-12-31T23:59:59.000Z]/fonts/",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36",
        "x-requested-with": "XMLHttpRequest",
    }

    page_range = "{}-{}".format(start_page, end_page)

    form_data = {
        "widget": "searchresults",
        "q": "release_date:[* TO 2020-12-31T23:59:59.000Z]",
        "nosamples": "1",
        "url": "/search/release_date:[*+TO+2020-12-31T23:59:59.000Z]/",
        "searchtype": "fonts",
        "embedded": "1",
        "endlessdir": "1",
        "range": page_range,  # eg: 51-100
        "ajax": "1",
    }

    res = r.post(SEARCH_RESULTS_URL, data=form_data, headers=headers)
    scrape_and_save(res)


if __name__ == "__main__":
    # initial search page scrape
    # do not run init if the original file is present 
    # if not os.path.exists(DUMP_FILE_NAME):
    #     init()
    SCRAPE_EVERY_INTERVAL = 51
    
    for i in range(51, 300, 51):
        time.sleep(2 * random.random())
        fetch_and_save_next_result_set(i, i + SCRAPE_EVERY_INTERVAL - 1)

    """
    next steps: 
        to be able to scrape on much large scale:
        1. At the start of script, read the existing excel file
        2. Identify the offset from which to start scraping again
    """
