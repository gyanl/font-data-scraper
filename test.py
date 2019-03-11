#Given a myfonts URL, extract all the tags.

from bs4 import BeautifulSoup
import csv
from requests import get
import re

list_names = []
list_creators = []
list_prices = []
list_styles = []

url = 'https://www.myfonts.com/search/release_date%3A%5B%2A+TO+2020-12-31T23%3A59%3A59.000Z%5D/fonts/'

response = get(url)

html_soup = BeautifulSoup(response.text, 'html.parser')
type(html_soup)

#Code for Font name
for link in html_soup('h4'):
    name = link.a.text
    list_names.append(name)
    #print(link.a.text, end=", ")

#Code for Font Foundry/Creator
for link in html_soup('div', class_ = 'long-description'):
    creator = link.a.text
    list_creators.append(creator)
    #print(link.a.text, end=", ")

#Code for Price
for link in html_soup('span', class_ = 'regular-price'):
    price = link.text
    list_prices.append(price)
    #print(link.a.text, end=", ")

#Code for Number of Styles
for link in html_soup('span', class_ = 'description'):
    style = int(re.search(r'\d+', link.text).group())
    list_styles.append(style)
    #print(link.text, end=", ")

print("Done!")


with open("fonts.csv", 'w', newline='') as myfile:
     wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
     wr.writerow(list_names)
     wr.writerow(list_creators)
     wr.writerow(list_styles)
     wr.writerow(list_prices)
