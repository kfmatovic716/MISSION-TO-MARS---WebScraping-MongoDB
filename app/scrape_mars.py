from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import pymongo
import requests
import pathlib
import pprint
import time

# Define a function called `scrape` that will execute all of your scraping code from the `mission_to_mars.ipynb` notebook
# Return one Python dictionary containing all of the scraped data. 
def scrape():

    # Set the executable path and initialize the chrome browser in splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    # Visit the mars nasa news site
    url_nasa = 'https://mars.nasa.gov/news/'

    # Optional delay for loading the page
    browser.visit(url_nasa)
# It will be a good idea to create multiple smaller functions that are called by the `scrape()` function. 
# Remember, each function should have one 'job' (eg. you might have a `mars_news()` function that scrapes the NASA mars news site and returns the content as a list/tuple/dictionary/json)
# HINT: the headers in the notebook can serve as a useful guide to where one 'job' ends and another begins. 

    def init_browser():
    executable_path = {"executable_path" : "chromedriver"}
    return Browser("chrome", **executable_path, headless = False)

def scrape():
    browser = init_browser()
    data = {}
    output = mars_news(browser)
    data['news_title'] = output[0]
    data['news_paragraph'] = output[1]
    data['mars_img'] = mars_img(browser)
    data['mars_weather'] = mars_weather(browser)
    data['mars_facts'] = mars_fact(browser)
    data['mars_hemisphere'] = mars_hemisphere(browser)
    return data

def mars_news(browser):
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)
    
    time.sleep(10)
 
    html = browser.html
    soup = bs(html, 'html.parser')
    article = soup.find('div', class_="list_text")
    news_title = article.find('div', class_="content_title").text
    news_p = article.find('div', class_= "article_teaser_body").text
    output = [news_title, news_p]
    return output

def mars_img(browser):
    url_mars_img = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url_mars_img)

    time.sleep(10)
    # Find and click the full image button

    html = browser.html
    soup = bs(html, "html.parser")
    img = soup.find('img', class_="thumb")['src']
    img_url = "https://www.jpl.nasa.gov/" +img
    return img_url

def mars_weather(browser):
    weather_url ="https://twitter.com/marswxreport?lang=en"
    browser.visit(weather_url)
    if browser.is_text_present('InSight sol', wait_time=10):

        html = browser.html
        soup = bs(html, "html.parser")
        a = soup.find('div', class_="css-901oao r-hkyrab r-1qd0xha r-a023e6 r-16dba41 r-ad9z0x r-bcqeeo r-bnwqim r-qvutc0")
        mars_weather = a.find('span', class_="css-901oao css-16my406 r-1qd0xha r-ad9z0x r-bcqeeo r-qvutc0").text.replace("\n", "")
    return mars_weather

def mars_fact(browser):
    import pandas as pd
    mars_facts_url = "https://space-facts.com/mars/"
    mars_df = pd.read_html(mars_facts_url)[0]
    mars_html = mars_df.to_html(header = False, index = False)
    return mars_html

def mars_hemisphere(browser):
    hemisphere_image_urls=[]
    mars_hem_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    
    time.sleep(10)

    browser.visit(mars_hem_url)
    html = browser.html
    soup = bs(html, "html.parser")
    list = soup.find_all('div', class_="item")
    for a in list:
        title = a.find('h3').text
        hem_url = "https://astrogeology.usgs.gov/" + a.find("a")["href"]
        browser.visit(hem_url)
        soup = bs(browser.html, 'html.parser')
        img_url = soup.find('li').find('a')['href']
        hemisphere_image_urls.append({'title': title, 'img_url': img_url})
    return hemisphere_image_urls