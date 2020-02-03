# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import datetime as dt
​
def scrape_all():
    # Initiate headless driver for deployment
    browser = Browser('chrome', 'chromedriver.exe', headless=False)
    # use our mars_news function to pull this data
    news_title, news_paragraph = mars_news(browser)
    # Run all scraping functions and store results in dictionary
    data = {"news_title": news_title, "news_paragraph": news_paragraph, "featured_image": featured_image(browser), "facts": mars_facts(), "last_modified": dt.datetime.now()}
    return data
​
# Set the executable path and initialize the chrome browser in splinter
browser = Browser('chrome', 'chromedriver.exe', headless=False)
​
# Create mars news function
def mars_news(browser):
    # Visit the mars nasa news site
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    # Optional delay for loading the page
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)
​
    # HTML parser
    html = browser.html
    news_soup = BeautifulSoup(html, 'html.parser')
    
    # Add try/except for error handling
    try:
        # Look for <ul /> and <li /> tags with classes item_list and slide
        slide_elem = news_soup.select_one('ul.item_list li.slide')
​
        # Scrape news titles
        slide_elem.find("div", class_='content_title')
​
        # Use the parent element to find the first `a` tag and save it as `news_title`
        news_title = slide_elem.find("div", class_='content_title').get_text()
        news_title
​
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_="article_teaser_body").get_text()
        news_p
    except AttributeError:
        return None, None
​
    return news_title, news_p
​
# ### Featured Images
def featured_image(browser):
​
    # Visit URL
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
​
    # Find and click the full image button
    full_image_elem = browser.find_by_id('full_image')
    full_image_elem.click()
​
    # Find the more info button and click that
​
    # First, the code makes sure an element is present using text. This tells Splinter to search through the HTML
    # for the specific text "more info." We can verify that it does exist in the HTML by using the DevTools to 
    # search for it. We also add a wait time of one second to make sure that everything in the page is finished 
    # loading before we search for it.
    browser.is_element_present_by_text('more info', wait_time=1)
​
    # Next, we create a new variable, more_info_elem, to find the link associated with the "more info" text.
    more_info_elem = browser.links.find_by_partial_text('more info')
​
    # Finally, we tell Splinter to click that link by chaining the .click() function onto our more_info_elem variable.
    more_info_elem.click()
​
    # Parse the resulting html with soup
    html = browser.html
    img_soup = BeautifulSoup(html, 'html.parser')
​
    # Find the relative image url
​
    # The <figure /> and <a /> tags have the image link nested within them.
​
    # figure.lede references the <figure /> tag and its class, lede
    # a is the next tag nested inside the <figure /> tag. Then <img />
    # .get("src") pulls the link to the image.
    try:
        img_url_rel = img_soup.select_one('figure.lede a img').get("src")
    except AttributeError:
        return None
​
    # Use the base URL to create an absolute URL
    img_url = f'https://www.jpl.nasa.gov{img_url_rel}'
​
    return img_url
​
# ### Space Facts Table
def mars_facts():
    try:
        # the [0] tells pandas to only pull the first table it sees
        df = pd.read_html('http://space-facts.com/mars/')[0]
    except BaseException:
        return None
    
    # Assign columns and set index of dataframe
    df.columns=['description', 'value']
​
    # inplace=True means that the updated index will remain in place, without having to reassign the
    # DataFrame to a new variable
    df.set_index('description', inplace=True)
​
    # converto df to html
    return df.to_html()
​
# ### Hemisphere Images
def hemi_images(browser):
​
    # Visit URL
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
​
    # Find and click the full image button
    full_image_elem = browser.find_by_text('Cerberus Hemisphere')
    full_image_elem.click()
​
    # Find the more info button and click that
​
    # First, the code makes sure an element is present using text. This tells Splinter to search through the HTML
    # for the specific text "more info." We can verify that it does exist in the HTML by using the DevTools to 
    # search for it. We also add a wait time of one second to make sure that everything in the page is finished 
    # loading before we search for it.
    browser.is_element_present_by_text('Cerberus Hemisphere', wait_time=1)
​
    # Next, we create a new variable, more_info_elem, to find the link associated with the "more info" text.
    cerberus = browser.links.find_by_partial_text('Cerberus Hemisphere')
​
    # Finally, we tell Splinter to click that link by chaining the .click() function onto our more_info_elem variable.
    cerberus.click()
​
    # Parse the resulting html with soup
    html = browser.html
    img_soup = BeautifulSoup(html, 'html.parser')
​
    # Find the relative image url
​
    # The <figure /> and <a /> tags have the image link nested within them.
​
    # figure.lede references the <figure /> tag and its class, lede
    # a is the next tag nested inside the <figure /> tag. Then <img />
    # .get("src") pulls the link to the image.
    try:
        img_url_rel = img_soup.select_one('figure.lede a img').get("src")
    except AttributeError:
        return None
​
    # Use the base URL to create an absolute URL
    cerb_img_url = f'https://astrogeology.usgs.gov/{img_url_rel}'
    print(cerb_img_url)
    return cerb_img_url
​
# close browswer
browser.quit() 
​
if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())