# Import dependencies splinter and BeautifulSoup
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
    # scraping functions and store results in dictionary
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
        url = 'https://mars.nasa.gov/news/'
        browser.visit(url)
        browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)
        html = browser.html
        n_soup = BeautifulSoup(html, 'html.parser')
        selements = n_soup.select_one('ul.item_list li.slide')
        # Use the parent element to find the first <a> tag and save it as `news_title`
        news_title = selements.find("div", class_='content_title').get_text()
        # Use the parent element to find the paragraph text
        news_p = selements.find('div', class_="article_teaser_body").get_text()
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
        # Parse the resulting html
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
    try:
        df = pd.read_html('http://space-facts.com/mars/')[0]
        df.columns=['Description', 'Mars']
        df.set_index('Description', inplace=True)
        return(df.to_html())
    except BaseException:
        return None

def cerb_hemi(browser):
    try:
        url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
        browser.visit(url)
        cerb_image = browser.find_by_text('Cerberus Hemisphere Enhanced', wait_time=1)
        cerb_image.click()
        html = browser.html
        imagesoup = BeautifulSoup(html, 'html.parser')
        cerbsoup = BeautifulSoup(html, 'html.parser')
        # Find the title
        cerberus_title = cerbsoup.find("h2", class_='title').get_text()
        cerberusSam = browser.links.find_by_partial_text('Sample')
        cerberusSam.click()
        # Find the relative image url
        cerb_url_rel = imagesoup.select_one('img.wide-image').get('src')
        # Use the base URL to create an absolute URL
        cerb_img_url = f'https://astrogeology.usgs.gov{cerb_url_rel}'
        return(cerb_img_url, cerberus_title)
    except AttributeError:
        return None, None
def schiap_hemi(browser):
    try:
        # Visit schiaparelli URL
        url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
        browser.visit(url)
        schiap_image = browser.find_by_text('Schiaparelli Hemisphere Enhanced')
        schiap_image.click()
        # Parse the resulting html with soup
        html = browser.html
        imagesoup = BeautifulSoup(html, 'html.parser')
        schiapsoup = BeautifulSoup(html, 'html.parser')
        # Find the title
        schiap_title = schiapsoup.find("h2", class_='title').get_text()
        schiaparelli = browser.links.find_by_partial_text('Sample')
        schiaparelli.click()
        # Find the relative image url
        schiap_url_rel = imagesoup.select_one('img.wide-image').get('src')
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
        syrtis_image = browser.find_by_text('Syrtis Major Hemisphere Enhanced')
        syrtis_image.click()
        # Parse the resulting html with soup
        html = browser.html
        image_soup = BeautifulSoup(html, 'html.parser')
        syrtissoup = BeautifulSoup(html, 'html.parser')
        # Find the title
        syrtis_title = syrtissoup.find("h2", class_='title').get_text()
        syrtis = browser.links.find_by_partial_text('Sample')
        syrtis.click()
        # Find the relative image url
        syrtis_url_rel = image_soup.select_one('img.wide-image').get('src')
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
        valles_image = browser.find_by_text('Valles Marineris Hemisphere Enhanced')
        valles_image.click()
        # Parse the resulting html with soup
        html = browser.html
        image_soup = BeautifulSoup(html, 'html.parser')
        vallessoup = BeautifulSoup(html, 'html.parser')
        # Find title
        valles_title = vallessoup.find("h2", class_='title').get_text()
        valles = browser.links.find_by_partial_text('Sample')
        valles.click()
        # Find the relative image url
        valles_url_rel = image_soup.select_one('img.wide-image').get('src')
        valles_img_url = f'https://astrogeology.usgs.gov{valles_url_rel}'
        return(valles_img_url, valles_title)
    except AttributeError:
        return None, None
#running scraped data
if __name__ == "__main__":
    print(scrape_all())
