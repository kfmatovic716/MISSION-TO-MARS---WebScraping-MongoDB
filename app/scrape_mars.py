from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import pymongo
import time

# Function `scrape` will execute all of scraping code from `mission_to_mars.ipynb`
# Return one Python dictionary containing all of the scraped data. 
def scrape():
    # Set the executable path and initialize the chrome browser in splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser_exec = Browser('chrome', **executable_path, headless=True)

    mars_data = {}
    news_output = mars_news(browser_exec)
    mars_data['news_title'] = news_output[0]
    mars_data['news_paragraph'] = news_output[1]
    mars_data['image'] = mars_image(browser_exec)
    mars_data['facts'] = mars_facts(browser_exec)
    mars_data['hemisphere'] = mars_hemispheres(browser_exec)
    return mars_data

# Scrapes NASA Mars News Site
# Pulls out latest news title and paragraph description
def mars_news(browser_exec):
    url_nasa = "https://mars.nasa.gov/news/"
    browser_exec.visit(url_nasa)
    
    time.sleep(5)
 
    html = browser_exec.html
    soup = BeautifulSoup(html, 'html.parser')

    latest_news = soup.findAll('div', class_="content_title")
    news_title = latest_news[1].text

    descriptions = soup.findAll('div', class_= "article_teaser_body")
    news_desc = descriptions[0].text

    news_output = [news_title, news_desc]

    return news_output

# Scrapes JPL Mars Space Image Site 
# Pulls out featured image of Mars
def mars_image(browser_exec):
    url_jpl = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    browser_exec.visit(url_jpl)

    time.sleep(5)

    html = browser_exec.html
    soup = BeautifulSoup(html, "html.parser")

    images = soup.findAll('img', class_="headerimage fade-in")
    featured_img = images[0].attrs['src']
    featured_img_url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/' + featured_img

    return featured_img_url

# Scrapes Space Facts Site
# Pulls out table with Mars facts and converts the table from Pandas to HTML format
def mars_facts(browser_exec):
    url_mars = "https://space-facts.com/mars/"
    browser_exec.visit(url_mars)

    rawdata_mars = pd.read_html(url_mars)[1]
    mars_df = rawdata_mars.rename(columns= {'Mars - Earth Comparison': 'Attributes'}).drop(columns = ["Earth"])

    mars_html_table = mars_df.to_html(index=False)

    return mars_html_table

# Scrapes Astrogeology USGS Site
# Pulls out high resolution images for each of Mar's hemispheres
# Results of image titles and urls are in list of dictionary format
def mars_hemispheres(browser_exec):
    base_url = "https://astrogeology.usgs.gov"
    url_hemisphere = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser_exec.visit(url_hemisphere) 

    time.sleep(5)

    html = browser_exec.html
    hem_soup = BeautifulSoup(html, "html.parser")

    results = hem_soup.find_all('div', class_="item")

    hem_img_urls = []
    for hem_img in results:
        hem_dict = {}

        href = hem_img.find('a', class_='itemLink product-item')
        link = base_url + href['href']
        browser_exec.visit(link)
        
        time.sleep(5)
        
        hem_html2 = browser_exec.html
        hem_soup2 = BeautifulSoup(hem_html2, 'html.parser')
        
        img_title = hem_soup2.find('div', class_='content').find('h2', class_='title').text
        hem_dict['title'] = img_title
        
        img_url = hem_soup2.find('div', class_='downloads').find('a')['href']
        hem_dict['url_img'] = img_url
        
        # Append dictionary to list
        hem_img_urls.append(hem_dict)

        return hem_img_urls