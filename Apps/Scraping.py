# Import Splinter and BeautifulSoup
import pandas as pd 
from splinter import Browser
from bs4 import BeautifulSoup
import datetime as dt

# Set the executable path and initialize the chrome browser in splinter
usersexecutable_path = {'executable_path': 'chromedriver.exe'}
browser = Browser('chrome', **usersexecutable_path, headless=False)

# Function to scrape all data
def scrape_all():
    news_title, news_paragraph = mars_news(browser)
    # Run all scraping functions and store results in dictionary
    data = {
    "news_title": news_title,
    "news_paragraph": news_paragraph,
    "featured_image": featured_image(browser),
    "facts": mars_facts(),
    "cerb_hemi": cerb_hemi(browser),
    "schap_hemi": schiap_hemi(browser),
    "syrtis_hemi": syrtis_hemi(browser),
    "valles_hemi": valles_hemi(browser),
    "last_modified": dt.datetime.now()
    }
    return(data)

#Function to pull mars_news
def mars_news(browser):
    try:
        #Visit the mars nasa news site
        url = 'https://mars.nasa.gov/news/'
        browser.visit(url)
        # Optional delay for loading the page
        browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)
        html = browser.html
        news_soup = BeautifulSoup(html, 'html.parser')
        slide_elem = news_soup.select_one('ul.item_list li.slide')
        # Use the parent element to find the first <a> tag and save it as `news_title`
        news_title = slide_elem.find("div", class_='content_title').get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_="article_teaser_body").get_text()
        return (news_title, news_p)
    except AttributeError:
        return None, None
#Fuction to pull featured_image
def featured_image(browser):
    try:
        url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
        browser.visit(url)
        # Find and click the full image button
        full_image_elem = browser.find_by_id('full_image')
        full_image_elem.click()
        # Find the more info button and click that
        browser.is_element_present_by_text('more info', wait_time=1)
        more_info_elem = browser.find_link_by_partial_text('more info')
        more_info_elem.click()
        # Parse the resulting html with soup
        html = browser.html
        img_soup = BeautifulSoup(html, 'html.parser')
        # Find the relative image url
        img_url_rel = img_soup.select_one('figure.lede a img').get("src")
        # Use the base URL to create an absolute URL
        img_url = f'https://www.jpl.nasa.gov{img_url_rel}'
        return(img_url)
        
    except AttributeError:
        return None
# Function to pull mars_facts
def mars_facts():
    # Add try/except for error handling
    try:
        # Use 'read_html' to scrape the facts table into a dataframe
        df = pd.read_html('http://space-facts.com/mars/')[0]
        # Assign columns and set index of dataframe
        df.columns=['Description', 'Mars']
        df.set_index('Description', inplace=True)
        # Convert dataframe into HTML format, add bootstrap
        return(df.to_html())
    except BaseException:
        return None
# Fuction to pull Ceberus hemisphere image and title
def cerb_hemi(browser):
    try:
# Visit  Cerberus URL
        url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
        browser.visit(url)
        # Find and click the Cerberus image button
        cerb_image_elem = browser.find_by_text('Cerberus Hemisphere Enhanced', wait_time=1)
        cerb_image_elem.click()
        # Parse the resulting html with soup
        html = browser.html
        img_soup = BeautifulSoup(html, 'html.parser')
        cerb_soup = BeautifulSoup(html, 'html.parser')
        # Find the title
        cerberus_title = cerb_soup.find("h2", class_='title').get_text()
        #cerberus_title
        # access the full resolution image
        #cerberus = browser.links.find_by_partial_text('cerberus_enhanced.tif')
        cerberus = browser.links.find_by_partial_text('Sample')
        cerberus.click()
        # Find the relative image url
        cerb_url_rel = img_soup.select_one('img.wide-image').get('src')
        #cerb_url_rel
        # Use the base URL to create an absolute URL
        cerb_img_url = f'https://astrogeology.usgs.gov{cerb_url_rel}'
        return(cerb_img_url, cerberus_title)
    except AttributeError:
        return None, None
# Fuction to pull Schiaparelli Hemisphere image and title
def schiap_hemi(browser):
    try:
        # Visit schiaparelli URL
        url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
        browser.visit(url)
        # Find and click the Schiaparelli image button
        schiap_image_elem = browser.find_by_text('Schiaparelli Hemisphere Enhanced')
        schiap_image_elem.click()
        # Parse the resulting html with soup
        html = browser.html
        img_soup = BeautifulSoup(html, 'html.parser')
        schiap_soup = BeautifulSoup(html, 'html.parser')
        # Find the title
        schiap_title = schiap_soup.find("h2", class_='title').get_text()
        #schiap_title
        # access the full resolution image
        #schiaparelli = browser.links.find_by_partial_text('schiap_enhanced.tif')
        schiaparelli = browser.links.find_by_partial_text('Sample')
        schiaparelli.click()
        # Find the relative image url
        schiap_url_rel = img_soup.select_one('img.wide-image').get('src')
        #schiap_url_rel
        # Use the base URL to create an absolute URL
        schiap_img_url = f'https://astrogeology.usgs.gov{schiap_url_rel}'
        return(schiap_img_url, schiap_title)
    except AttributeError:
        return None, None
# Fuction for Syrtis Major Hemisphere
def syrtis_hemi(browser):
    try:
        # Visit Syrtis major URL
        url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
        browser.visit(url)
        # Find and click the Schiaparelli image button
        syrtis_image_elem = browser.find_by_text('Syrtis Major Hemisphere Enhanced')
        syrtis_image_elem.click()
        # Parse the resulting html with soup
        html = browser.html
        img_soup = BeautifulSoup(html, 'html.parser')
        syrtis_soup = BeautifulSoup(html, 'html.parser')
        # Find the title
        syrtis_title = syrtis_soup.find("h2", class_='title').get_text()
        #syrtis_title
        # access the full resolution image
        #schiaparelli = browser.links.find_by_partial_text('schiap_enhanced.tif')
        syrtis = browser.links.find_by_partial_text('Sample')
        syrtis.click()
        # Find the relative image url
        syrtis_url_rel = img_soup.select_one('img.wide-image').get('src')
        #syrtis_url_rel
        # Use the base URL to create an absolute URL
        syrtis_img_url = f'https://astrogeology.usgs.gov{syrtis_url_rel}'
        return(syrtis_img_url, syrtis_title)
    except AttributeError:
        return None, None
def valles_hemi(browser):
    try:
        # Visit Valles Marineris URL
        url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
        browser.visit(url)
        # Find and click the Schiaparelli image button
        valles_image_elem = browser.find_by_text('Valles Marineris Hemisphere Enhanced')
        valles_image_elem.click()
        # Parse the resulting html with soup
        html = browser.html
        img_soup = BeautifulSoup(html, 'html.parser')
        valles_soup = BeautifulSoup(html, 'html.parser')
        # Find title
        valles_title = valles_soup.find("h2", class_='title').get_text()
        #valles_title
        # access the full resolution image
        #schiaparelli = browser.links.find_by_partial_text('schiap_enhanced.tif')
        valles = browser.links.find_by_partial_text('Sample')
        valles.click()
        # Find the relative image url
        valles_url_rel = img_soup.select_one('img.wide-image').get('src')
        #valles_url_rel
        # Use the base URL to create an absolute URL
        valles_img_url = f'https://astrogeology.usgs.gov{valles_url_rel}'
        return(valles_img_url, valles_title)
    except AttributeError:
        return None, None
#running scraped data
if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())