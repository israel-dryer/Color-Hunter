# Color-Hunter
 A program for scraping color themes from the [colorhunt website](https://colorhunt.co/palettes)
 
 The [color_hunter.py](color_hunter.py) script downloads all available color themes. You may need to adjust the `sleep()` time depending on your internet connection. This allows the screen to load while scrolling down the page to load more data.  
 
 The script will return a dictionary containing an ID and a tuple of hexadecimal colors, the last of which is a text color of black or white, which has been programmed based on the best contrast of the primary color (index 0) in the tuple.
 
 Required installation
 - [Google Chrome](https://www.google.com/chrome/)
 - [Chromedriver](https://chromedriver.chromium.org/)
 
 The `chromedriver.exe` file should be saved in a directory that is accessible from **PATH**. You may put it into the same folder as your `python.exe` file if you wish, or pass the path as a parameter in `webdriver()`. 
 
Other required libraries (Python 3.7):
```
pip install selenium
pip install bs4
```

Documentation is available for the relevant libraries:
- [selenium](https://selenium-python.readthedocs.io/)
- [bs4 - BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
