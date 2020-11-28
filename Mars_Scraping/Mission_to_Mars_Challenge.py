#!/usr/bin/env python
# coding: utf-8

# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd

# Path to chromedriver
get_ipython().system('which chromedriver')

# Set the executable path and initialize the chrome browser in splinter
browser = Browser('chrome', executable_path='/Users/redheadedmath/.wdm/drivers/chromedriver/mac64/86.0.4240.22/chromedriver', headless=True)

# ### Visit the NASA Mars News Site

# Visit the mars nasa news site
url = 'https://mars.nasa.gov/news/'
browser.visit(url)

# Optional delay for loading the page
browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)

# Convert the browser html to a soup object and then quit the browser
html = browser.html
news_soup = soup(html, 'html.parser')

slide_elem = news_soup.select_one('ul.item_list li.slide')
slide_elem.find("div", class_='content_title')

# Use the parent element to find the first a tag and save it as `news_title`
news_title = slide_elem.find("div", class_='content_title').get_text()

# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_="article_teaser_body").get_text()

# ### JPL Space Images Featured Image

# Visit URL
url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
browser.visit(url)

# Find and click the full image button
full_image_elem = browser.find_by_id('full_image')
full_image_elem.click()

# Find the more info button and click that
browser.is_element_present_by_text('more info', wait_time=1)
more_info_elem = browser.links.find_by_partial_text('more info')
more_info_elem.click()

# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')

# find the relative image url
img_url_rel = img_soup.select_one('figure.lede a img').get("src")

# Use the base url to create an absolute url
img_url = f'https://www.jpl.nasa.gov{img_url_rel}'

# ### Mars Facts
df = pd.read_html('http://space-facts.com/mars/')[0]
df.columns=['Description', 'Mars']
df.set_index('Description', inplace=True)
df.to_html()

# ### Mars Weather

# Visit the weather website
url = 'https://mars.nasa.gov/insight/weather/'
browser.visit(url)

# Parse the data
html = browser.html
weather_soup = soup(html, 'html.parser')

# Scrape the Daily Weather Report table
weather_table = weather_soup.find('table', class_='mb_table')
print(weather_table.prettify())

# ### Hemispheres

# 1. Use browser to visit the URL 
url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
browser.visit(url)

# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []
click_urls = ["Cerberus Hemisphere Enhanced", "Schiaparelli Hemisphere Enhanced",
             "Syrtis Major Hemisphere Enhanced", "Valles Marineris Hemisphere Enhanced"]
# 3. Write code to retrieve the image urls and titles for each hemisphere.
# not pretty, but it gets the job done. 
for item in click_urls:
    browser.visit(url)
    thumbnail = browser.find_by_text(item)
    thumbnail.click()
    html = browser.html
    high_res_soup = soup(html, 'html.parser')
    img_url = high_res_soup.select_one('div.downloads ul li a').get("href")
    title = high_res_soup.select_one('div.content section h2').get_text()
    hemi_dict = {'img_url':img_url,
                 'title':title}
    hemisphere_image_urls.append(hemi_dict)

# 4. Print the list that holds the dictionary of each image url and title.
#hemisphere_image_urls

# 5. Quit the browser
browser.quit()