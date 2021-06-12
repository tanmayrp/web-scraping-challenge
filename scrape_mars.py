from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

def scrape():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    ##################################################
    # NASA Mars News
    # Scrape the Mars News Site and collect the latest News Title and Paragraph Text to be referenced later.
    ##################################################
    # Website to Scrape data
    url = 'https://redplanetscience.com/'
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # Scrape the site to find all news titles
    titles = soup.find_all('div', class_='content_title')
    news_title = []
    for title in titles:
        news_title.append(title.text)

    # Scrape the site to find all news paragraphs
    paragraphs = soup.find_all('div', class_='article_teaser_body')
    news_p = []
    for paragraph in paragraphs:
        news_p.append(paragraph.text)

    ##################################################
    # JPL Mars Space Images - Featured Image
    # Visit the specified URL, use splinter to navigate the site and find the image url fo rhte current Featured Mars Image.
    ##################################################
    url = 'https://spaceimages-mars.com/'
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # Retrieve image url
    div_data=soup.find_all('div', class_='floating_text_area')

    # Go through data and find the image href
    for div in div_data:
        image_url = div.find('a')['href']

    # Join the url with image_url to create the fully qualified image_url to be used
    featured_image_url = url + image_url

    ##################################################
    # Mars Facts
    # Visit the specified URL, scrape the table containing facts about the planet, 
    # includign Diameter, Mass etc. Use Pandas to convert the data to a HTML table string
    ##################################################
    url = 'https://galaxyfacts-mars.com/'

    # Read tables 
    tables = pd.read_html(url)

    # Use first table found to operate on
    df = tables[0]

    # Rename columns, reset index, and drop the first row as its unnecessary
    df=df.rename(columns={0: "Description", 1:"Mars",2:"Earth"})
    df = df.reset_index(drop=True)
    df.drop(index=df.index[0], axis=0, inplace=True)
    final_df = df.set_index('Description')

    # Convert dataframe into html table
    html_table = final_df.to_html(classes='table table-striped table-bordered')
    html_table = html_table.replace('\n','')

    ##################################################
    # Mars Hemispheres
    # Visit the specified URL, click links in order to find the image url to the 
    # full res image. Save image url and title into a Python dictionary. Append 
    # the dicutionary with the image url string and the hemisphere title to a list. 
    # The list will contain one dictionary for each hemisphere.
    ##################################################
    url='https://marshemispheres.com/'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    items=soup.find_all('div', class_='item')
    hemisphere_image_urls  = []

    # Loop through each hemisphere item
    for item in items:
        try:
            # Find title and append it to list
            hemisphere = item.find('div',class_='description')
            hemisphere_title = hemisphere.h3.text
            
            # Find image urls
            hemisphere_url = item.find('a')['href']
            
            # Visit the URL and extract the image link
            browser.visit(url + hemisphere_url)
            html = browser.html
            soup = BeautifulSoup(html, 'html.parser')
            image_url = soup.find('li').a['href']
            
            # Add title and image to a dictionary
            hemisphere_dictionary = {
                "title" : hemisphere_title,
                "img_url" : url + image_url
            }
            
            # Add dictionary to a list
            hemisphere_image_urls.append(hemisphere_dictionary)
            
        except Exception as e:
            print(e)

    # Store data in a dictionary
    mars_info_dictionary = {
        "news_title" : news_title,
        "news_p" : news_p,
        "featured_image_url" : featured_image_url,
        "html_table" : html_table,
        "hemisphere_image_urls" : hemisphere_image_urls
    }

    # Close the browser after scraping
    browser.quit()
    
    # Return results
    return mars_info_dictionary