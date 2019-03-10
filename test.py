#Given a myfonts URL, extract all the tags.

from bs4 import BeautifulSoup

from requests import get

url = 'http://www.myfonts.com/fonts/northernblock/moret/'

response = get(url)

html_soup = BeautifulSoup(response.text, 'html.parser')
type(html_soup)

#Code for printing font weights
print("Foundry, Weights : ", end=" ")

for link in html_soup.find_all('h4'):
    print(link.a.text, end=", ")

print("")

#Code for printing tags
print("Tags : ", end=" ")

for link in html_soup.find_all('span', class_ = 'tag'):
    print(link.text, end=", ")

print("")
