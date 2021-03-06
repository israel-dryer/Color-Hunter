"""
    Color Hunter - A script for scraping color themes from the colorhunt.co website
    Author      :   Israel Dryer
    Modified    :   2019-11-14
"""
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from time import sleep
import requests

# ---- scrape colors from internet -------------------------------------------
chrome_options = Options()
chrome_options.add_argument("--dns-prefetch-disable")
chrome_options.add_argument("--no-proxy-server")
bot = webdriver.Chrome(options=chrome_options)

url = "https://colorhunt.co/palettes"

# navigate to the target url
bot.get(url)

# scroll to bottom of page to load all palettes
last_height = bot.execute_script("return document.body.scrollHeight")
while True:
    bot.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    sleep(1.25) # may need to adjust based on lag and connection speed
    new_height = bot.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break    
    last_height = new_height

# extract color palettes from html source
soup = BeautifulSoup(bot.page_source)
pal = soup.find_all("div",{"class":"palette"})
bot.quit()

# iterate through each color palette and save to themes
themes = {}
for row in pal:
    color = row.find_all('div')
    c1 = color[3].text
    c2 = color[2].text 
    c3 = color[1].text
    c4 = color[0].text
    theme_name = color[0].a['href'].split('/').pop()
    if theme_name:
        themes[theme_name] = (c1, c2, c3, c4)

# add hash tags to aid in theme naming
for key, val in themes.items():
    r = requests.get(f'https://colorhunt.co/palette/{int(key)}')
    soup = BeautifulSoup(r.text)
    scripts = soup.find_all('script')
    hash_script = scripts[7]
    hashes = hash_script.text.split(';')
    for row in hashes:
        if row.strip()[:5] == 'focus':
            key_hashes = row.strip().replace('focus','').replace('(','').replace(')','').replace("'",'').split()
            themes[key] = val + (key_hashes,)
            break
    # add small delay to prevent exceeding url request limit
    sleep(0.05)

# export colors to python file
with open('themes_dict.py','w') as f:
    f.write('themes = {\n')
    for key, val in themes.items():
        f.write(f"\t'{key}': {val},\n")
    f.write('}')

print('Scraping complete!')