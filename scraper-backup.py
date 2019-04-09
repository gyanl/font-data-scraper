#Given a myfonts URL, extract all the tags.

from bs4 import BeautifulSoup
import pandas
from requests import get
import re

i=0
list_of_fonts = []

list_names = []
list_creators = []
list_prices = []
list_styles = []

url = 'https://www.myfonts.com/search/release_date%3A%5B%2A+TO+2020-12-31T23%3A59%3A59.000Z%5D/fonts/'

response = get(url)

html_soup = BeautifulSoup(response.text, 'html.parser')
type(html_soup)


font_containers = html_soup.find_all('div', class_ = 'search-result-item')
print(len(font_containers))

for container in font_containers:
    i=i+1;
    #Code for Font name
    #for link in html_soup('h4'):
    name = container.h4.a.text
    list_names.append(name)
    #print(link.a.text, end=", ")

    #Code for Font Foundry/Creator
    #for link in html_soup('div', class_ = 'long-description'):
    creator = container.find('div', class_ = 'long-description').a.text
    list_creators.append(creator)
    #print(link.a.text, end=", ")

    #Code for Price
    #for link in html_soup('span', class_ = 'regular-price'):
    price = container.find('span', class_ = 'regular-price').text
    list_prices.append(price)
    #print(link.a.text, end=", ")

    #Code for Number of Styles
    #for link in html_soup():
    style = int(re.search(r'\d+', container.find('span', class_ = 'description').text).group())
    list_styles.append(style)
    #print(link.text, end=", ")

    print(i, end =" ")

print("Done!")

df = pandas.DataFrame(data={"Font Name": list_names, "Foundry/Creator": list_creators, "Price": list_prices, "Styles": list_styles})
df.to_csv("./fonts.csv", sep=',',index=False)
