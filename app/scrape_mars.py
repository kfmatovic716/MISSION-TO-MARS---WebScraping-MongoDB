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
    mars_data['hemis'] = mars_hemispheres(browser_exec)
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

    mars_html_table = mars_df.to_html(header=False, index=False)

    return mars_html_table

# Scrapes Astrogeology USGS Site
# Pulls out high resolution images for each of Mar's hemispheres
# Results of image titles and urls are in list of dictionary format
def mars_hemispheres(browser_exec):
    base_url = "https://astrogeology.usgs.gov"
    url_hemisphere = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser_exec.visit(url_hemisphere) 

    time.sleep(1)

    hem_html = browser_exec.html
    hem_soup = BeautifulSoup(hem_html, "html.parser")

    hem_img_urls = []
    image_titles = hem_soup.findAll('h3')

    for i in range(len(image_titles)):
        hemisphere = {}
        
        img_title = hem_soup.findAll('h3')[i].text
        
        img_url = base_url + hem_soup.findAll('a', class_='itemLink product-item')[i]['href']
        browser_exec.visit(img_url)

        time.sleep(1)

        html = browser_exec.html
        soup = BeautifulSoup(html, 'html.parser')

        final_img_url = soup.find('div', class_='downloads').find('a')['href']
        
        hemisphere["title"] = img_title
        hemisphere["img_url"] = final_img_url
        
        hem_img_urls.append(hemisphere)    

    return hem_img_urls