from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
import pandas as pd

def scrape_mars():
    def init_browser():
        # @NOTE: Replace the path with your actual path to the chromedriver
        executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
        return Browser("chrome", **executable_path, headless=False)

    #PART 1
    browser = init_browser()

    # Visit nasa.gov/news
    url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    browser.visit(url)

    time.sleep(1)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    #Digs through the html page in order to get tot he list of titles.
    #Could've been more efficient but ¯\_(ツ)_/¯
    main = soup.find('div', id='main_container')
    body = main.find('div', id='site_body')
    page = body.find('div', id='page')
    grid_list = page.find_all('div')
    grid_list = grid_list[1]
    div_list = grid_list.find_all('div')
    new_list = div_list[1]
    section = new_list.find('section')
    layout = section.find('div')
    ul = layout.find('ul')
    ul_list = ul.find_all('li')
    n = ul_list[0].find_all('div')

    #The structure of our data is going to be a dictionary of dictionaries. The key to the top
    #dictionary (news_dict) will be news_date and the value will be title_dict. Inside title_dict
    #the key:value pairs will be Title:news_title and Paragraph:news_paragraph.


    news_dict = {}

    for u in ul_list:
        title_dict = {}
        divs = u.find_all('div')
        news_title = divs[9].text
        news_date = divs[8].text
        news_paragraph = divs[10].text
        title_dict['Title'] = news_title
        title_dict['Paragraph'] = news_paragraph
        news_dict[news_date] = title_dict
    
    browser.quit()

    #PART 2
    browser = init_browser()

    # Getting images

    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    time.sleep(1)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    #A little more efficient, but could be better.
    ul_list = soup.find_all('div')
    main = ul_list[0]
    page = main.find_all('div', id='page')
    images = page[0].find_all('img')

    url_extensions = []
    for image in images:
        split = str(image).split('src="')
        url_ext_list = split[1].split('"/>')
        non_title = url_ext_list[0].split(' ')
        url_ext = non_title[0]
        if 'jpg' in url_ext:
            url_extensions.append('https://www.jpl.nasa.gov' + url_ext)

    browser.quit()

    #PART 3

    browser = init_browser()

    # Visit mars twitter

    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)

    time.sleep(1)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    #Ok I'm finally kinda getting the hang of this.
    tweets = soup.body.find_all('div', class_='js-tweet-text-container')

    weathers = []

    for tweet in tweets:
        split = tweet.p.text.split('hPapic')
        if 'InSight' in split[0]:
                weathers.append(split[0])

    browser.quit()

    #PART 4

    url = 'https://space-facts.com/mars/'
    tables = pd.read_html(url)

    table_strings = []
    for table in tables:
        html_table = table.to_html()
        html_table = html_table.replace('\n', '')
        table_strings.append(html_table)
    
    
    #PART 5
    # Visit all four of the image pages
    urls = ['https://astrogeology.usgs.gov/search/map/Mars/Viking/valles_marineris_enhanced.tif', 
            'https://astrogeology.usgs.gov/search/map/Mars/Viking/cerberus_enhanced',
            "https://astrogeology.usgs.gov/search/map/Mars/Viking/schiaparelli_enhanced",
            "https://astrogeology.usgs.gov/search/map/Mars/Viking/syrtis_major_enhanced"]

    image_urls = []

    for url in urls:
        browser = init_browser()
        
        browser.visit(url)

        time.sleep(1)

        # Scrape page into Soup
        html = browser.html
        soup = bs(html, "html.parser")
        #Finds the image URL extension
        image = soup.find('img', class_="wide-image")
        image = str(image).split()
        image = image[2].split('src="')
        image = image[1].split('"')
    
        #Finesses the data so that the url is whole and appends it to a list.
        image_urls.append(f"https://astrogeology.usgs.gov{image[0]}")
        browser.quit()

    hemisphere_image_urls = [
    {"title": "Valles Marineris Hemisphere", "img_url": image_urls[0]},
    {"title": "Cerberus Hemisphere", "img_url": image_urls[1]},
    {"title": "Schiaparelli Hemisphere", "img_url": image_urls[2]},
    {"title": "Syrtis Major Hemisphere", "img_url": image_urls[3]}
    ]

    final_dict = {'Part One': news_dict, 
    'Part Two': url_extensions, 'Part Three': weathers, 
    'Part Four': table_strings , 'Part Five': hemisphere_image_urls} 

    return final_dict




    


    
