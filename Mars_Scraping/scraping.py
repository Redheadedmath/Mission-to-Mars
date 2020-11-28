#!/usr/bin/env python
# coding: utf-8
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime as dt

def scrape_all():
    #Initialize headless driver for deployment
    browser = Browser('chrome', executable_path='/Users/redheadedmath/.wdm/drivers/chromedriver/mac64/86.0.4240.22/chromedriver', headless=True)

    news_title, news_paragraph = mars_news(browser)
    hemispheres = high_res_dict(browser)

    # Run all scraping functions and store results in dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now(),
        "hemispheres": hemispheres
    }
    #Stop webdriver and return data
    browser.quit()
    return data


def mars_news(browser):

    # Scrape Mars News
    # Visit the mars nasa news site
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)

    # Convert browser html to soup object for parsing
    html = browser.html
    news_soup = soup(html, 'html.parser')

    # Add try/except for erros
    try:
        slide_elem = news_soup.select_one('ul.item_list li.slide')
        slide_elem.find("div", class_='content_title')
        # Use the parent element to find the first `a` tag and save it as `news_title`
        news_title = slide_elem.find("div", class_='content_title').get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_="article_teaser_body").get_text()
    
    except AttributeError:
        return None, None

    return news_title, news_p

# ### Featured Images
def featured_image(browser):

    # Visit URL
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    # Find and click the full image button
    full_image_elem = browser.find_by_id('full_image')[0]
    full_image_elem.click()
    # Find the more info button and click that
    browser.is_element_present_by_text('more info', wait_time=1)
    more_info_elem = browser.links.find_by_partial_text('more info')
    more_info_elem.click()
    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    #try-except clause for errors 
    try:
        # Find the relative image url
        img_url_rel = img_soup.select_one('figure.lede a img').get("src")
    except AttributeError:
        return None
    # Use the base URL to create an absolute URL
    img_url = f'https://www.jpl.nasa.gov{img_url_rel}'

    return img_url

def mars_facts():
    # try-except for errors
    try:
        df = pd.read_html('http://space-facts.com/mars/')[0]
    except BaseException:
        return None
    # Assign Columns and set index of dataframe
    df.columns=['Description','Mars']
    df.set_index('Description', inplace=True)

    # Return to html format, add bootstrap
    return df.to_html(classes="table table-striped")

def high_res_dict(browser):
    #establish target URL
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars' 
    #create repository list for dictionaries
    hemisphere_image_urls = []
    #iterable list of known headers
    click_urls = ["Cerberus Hemisphere Enhanced", "Schiaparelli Hemisphere Enhanced",
             "Syrtis Major Hemisphere Enhanced", "Valles Marineris Hemisphere Enhanced"]
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

    return hemisphere_image_urls

if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())