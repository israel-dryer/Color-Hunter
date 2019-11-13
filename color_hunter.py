"""
    Color Hunter - A script for scraping color themes from the colorhunt.co website
    Author      :   Israel Dryer
    Modified    :   2019-11-13
"""
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from time import sleep

# setup page scraper
chrome_options = Options()
chrome_options.add_argument("--dns-prefetch-disable")
chrome_options.add_argument("--no-proxy-server")
bot = webdriver.Chrome(chrome_options=chrome_options)

themes = {} # store collected themes
url = "https://colorhunt.co/palettes"

# navigate to the target url
bot.get(url)

# scroll to bottom of page to load all palettes
last_height = bot.execute_script("return document.body.scrollHeight")
while True:
    bot.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    sleep(2) # may need to adjust based on lag and connection speed
    new_height = bot.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break    
    last_height = new_height

# extract color palettes from html source
soup = BeautifulSoup(bot.page_source, 'lxml')
pal = soup.find_all("div",{"class":"palette"})

# iterate through each color palette and save to themes
for row in pal:
    color = row.find_all('div')
    c1 = color[3].text
    c2 = color[2].text 
    c3 = color[1].text
    c4 = color[1].text
    theme_name = color[0].a['href'].split('/').pop()
    themes[theme_name] = (c1, c2, c3, c4)

bot.close()

# write dictionary to python file
with open('colors.py','w') as f:
    f.write('color_hunt = {\n')
    for key, val in themes.items():
        f.write(f"\t'{key}': {val},\n")
    f.write('}')

