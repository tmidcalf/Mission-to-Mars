# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt
from webdriver_manager.chrome import ChromeDriverManager


def scrape_all():

    # Initiate headless driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    news_title, news_paragraph = mars_news(browser)

    # Run all scraping functions and store results in dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now(),
        "hemispheres": hemisphere_info(browser)
    }
    # Stop webdriver and return data
    browser.quit()
    return data


def mars_news(browser):

    # Visit the mars nasa news site
    url = 'https://redplanetscience.com'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')
    
    # Add try/except for error handling
    try:

        slide_elem = news_soup.select_one('div.list_text')
        # Use the parent element to find the first `a` tag and save it as `news_title`
        news_title = slide_elem.find('div', class_='content_title').get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
    
    except AttributeError:
        return None, None   
    
    return news_title, news_p

# ## JPL Space Images Featured Image

def featured_image(browser):

    # Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')
    
    try:
        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
    
    except AttributeError:
        return None

    # Use the base URL to create an absolute URL
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'

    return img_url

# ## Mars Facts

def mars_facts():
    try:
        # use 'read_html" to scrape the facts table into a dataframe
        df = pd.read_html('https://galaxyfacts-mars.com')[0]
    
    except BaseException:
        return None

    # Assign columns and set index of dataframe
    df.columns=['description', 'Mars', 'Earth']
    df.set_index('description', inplace=True)

    table_classes = "table table-striped"
    return df.to_html(classes=table_classes)

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


if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())


