# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt
from webdriver_manager.chrome import ChromeDriverManager


def hemisphere_info(browser):
    # Visit URL
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

    # Initiate a list to hold the image URL strings and titles
    hemisphere_urls = []

    for x in range(4):
        # Click the link to the image
        browser.find_by_tag('h3')[x].click()
        
        # Parse the resulting html with soup
        hem_soup = soup(browser.html, 'html.parser')
        
        # Define the text to search by
        text = "Sample"
        
        # Search by text with the help of lambda function and get the img URL
        hem_url = hem_soup.find_all(lambda tag: tag.name == "a" and text in tag.text)[0].get('href')
        
        # Get the title
        title = hem_soup.find('h2', class_='title').get_text()
        
        # Add a dictionary with the img URL and title to the list
        hemisphere_urls.append({'img_url': hem_url,
                            'title': title})
        
        # Return to the pervious page
        browser.back()

    return hemisphere_urls


