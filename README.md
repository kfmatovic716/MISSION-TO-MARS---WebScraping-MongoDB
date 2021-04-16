# Mission-to-Mars - A Web Scraping Adventure
![](https://github.com/kfmatovic716/Webscraping-Mission-to-Mars/blob/main/images/mission_to_mars.png?raw=true)

## Objectives:
<ol>
    <li>To extract data via Web Scraping using Jupyter notebook, and Pandas, BeautifulSoup, & Splinter/Requests python libraries </li>
    <li>To use MongoDB with Flask templating (Jinja) to create a new HTML page that displays all the scraped information </li>
</ol>

## Web Scraping 
<ul>
    <li>The following sites were visited for Web Scraping:</li>
        <ul>
            <li><a href="https://mars.nasa.gov/news/">NASA Mars News Site</a>- latest news title and paragraph text</li>
            <li><a href="https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html">JPL Mars Space Images</a>- Mars featured image in space</li>
            <li><a href="https://space-facts.com/mars/">Space Facts Site</a>- Mars facts table</li>
            <li><a href="https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars">USGS Astrogeology Site</a>- high resolution images of hemispeheres in Mars</li>
        </ul>
    <li>scrape_mars.py - Jupyter notebook converted to a Python script that contains the "scrape" function that will execute all of your scraping code from above and returns one Python dictionary containing all of scraped data</li>
</ul>

## Mongo DB and Flask Application
<ul>
    <li>app.py - is a Flask application that will import the `scrape` function from `scrape_mars`. The following routes are available in this app</li>
        <ul>
            <li>a root route `/` that will query the Mongo database and pass the mars data into an HTML template to display the data</li>
            <li>`/scrape` route that imports scrape_mars.py and calls the `scrape` function then stores the return value as a Python dictionary</li>
        </ul>
    <li>index.html - an html file using Jinja templating that will take the mars data dictionary and display all of the data in the appropriate HTML elements</li>
</ul>

![](https://github.com/kfmatovic716/Webscraping-MongoDB-Mission-to-Mars/blob/main/images/final_app1.PNG?raw=true)
![](https://github.com/kfmatovic716/Webscraping-MongoDB-Mission-to-Mars/blob/main/images/final_app2.PNG?raw=true)
![](https://github.com/kfmatovic716/Webscraping-MongoDB-Mission-to-Mars/blob/main/images/final_app3.PNG?raw=true)