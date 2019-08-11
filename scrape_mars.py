# Import Dependencies
from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
import pymongo

# Initiate browser
def init_browser():
    executable_path = {'executable_path': 'C:\\Users\\Public\\chromedriver.exe'}
    return Browser("chrome", **executable_path, headless=False)

# Scrape info and keep in dictionary that will be used through mongo in the app.py
def scrape():
    browser = init_browser()
    mars_data = {}


    # NASA Mars News
    news_url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    browser.visit(news_url)
    html = browser.html


    news_soup = bs(html, 'html.parser')
    news_title = news_soup.find('div', class_='content_title').text.strip()
    news_p = news_soup.find('div', class_='rollover_description_inner').text.strip()

    mars_data["title"] = news_title
    mars_data["paragraph"] = news_p


    # JPL Mars Space Images - Featured Image
    jpl_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(jpl_url)
    html = browser.html


    jpl_soup = bs(html, 'html.parser')
    jpl_image = jpl_soup.find('a', class_='button fancybox')['data-fancybox-href']
    featured_image_url = 'https://www.jpl.nasa.gov' + jpl_image

    mars_data["featured_image"] = featured_image_url



    # Mars Weather
    weather_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(weather_url)
    html = browser.html

    weather_soup = bs(html, 'html.parser')
    mars_weather = weather_soup.find('p', class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text').text.strip()

    mars_data["weather"] = mars_weather


    # Mars Facts
    facts_url = 'https://space-facts.com/mars/'
    browser.visit(facts_url)

    tables = pd.read_html(facts_url)
    df = tables[0]
    html_table = df.to_html()
    html_table.replace('\n', '')

    # Mars Hemispheres
    hemi_url = 'http://www.planetary.org/blogs/guest-blogs/bill-dunford/20140203-the-faces-of-mars.html'
    browser.visit(hemi_url)
    html = browser.html

    hemi_soup = bs(html, 'html.parser')
    hemispheres = hemi_soup.find_all('img', class_='img840')

    hemisphere_image_urls = []
    for hemisphere in hemispheres:
        hemisphere_dict = {}
        hemisphere_dict["title"] = hemisphere['alt']
        hemisphere_dict["img_url"] = hemisphere['src']
        hemisphere_image_urls.append(hemisphere_dict)


    mars_data["hemispheres"] = hemisphere_image_urls

    browser.quit()
    return mars_data