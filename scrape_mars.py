#!/usr/bin/env python
# coding: utf-8

# Mars ain't the kind of place to raise a kid  
# In fact, it's cold as hell.
#            - Elton John, "Rocket Man"



from bs4 import BeautifulSoup as bs
import requests
from splinter import Browser
import pandas as pd
import time

def init_browser():
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


def scrape_info():
    # ## Get Mars News
    executable_path = {"executable_path" : "chromedriver.exe"}
    browser = Browser("chrome", **executable_path, headless=False)

    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    html = browser.html
    soup = bs(html, 'html.parser')

    news_title = soup.find("div", class_="content_title").text
    news_p     = soup.find("div", class_="article_teaser_body").text

    # ## Get Mars Featured Image
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)
    browser.click_link_by_partial_text("FULL IMAGE")
    time.sleep(3)
    browser.click_link_by_partial_text("more info")

    html = browser.html
    soup = bs(html, 'html.parser')
    
    featured_image = soup.find("figure", class_="lede")
    print(featured_image)

    featured_image_url = "https://www.jpl.nasa.gov" + featured_image.find("a")["href"]
    print(featured_image_url)


    # ## Get Mars Weather

    url = 'https://twitter.com/marswxreport?lang=en'
    response = requests.get(url)
    soup = bs(response.text, 'lxml')

    def getText(parent):
        return ''.join(parent.find_all(text=True, recursive=False)).strip()

    result = soup.find("p", class_="tweet-text")
    weather_report = getText(result)
    print(weather_report)


    # ## Get Mars Facts

    url = "https://space-facts.com/mars/"
    response = requests.get(url)
    soup = bs(response.text, "lxml")

    result_labels = soup.find_all("td", class_="column-1")
    result_values = soup.find_all("td", class_="column-2")

    result_labels_text = []
    result_values_text = []
    for rlabel in result_labels:
        result_labels_text.append(rlabel.text)
    for rvalue in result_values:
        result_values_text.append(rvalue.text)

    mars_df = pd.DataFrame({"Stats": result_labels_text,
                            "Values":  result_values_text})

    mars_df.set_index("Stats",inplace=True)
    
    mars_facts_html = mars_df.to_html()
   
    # ## Get Hemisphere Images

    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)

    hemisphere_list = []

    hemispheres = ["Cerberus", "Schiaparelli", "Syrtis Major", "Valles Marineris"]
    for x in range(0,4):
        browser.click_link_by_partial_text(hemispheres[x])
        
        html = browser.html
        soup = bs(html, 'html.parser')
        
        img_url = "https://astrogeology.usgs.gov" + (soup.find("img", class_="wide-image")["src"])
        title = (soup.find("h2", class_="title").text)
        
        hemisphere_dict = {"title": title, "img_url":img_url}
        hemisphere_list.append(hemisphere_dict)
        
        browser.back()
 
    browser.quit()

        # Store data in a dictionary
    mars_data = {
        "news_title": news_title,
        "news_p": news_p,
        "featured_image_url": featured_image_url,
        "weather_report" : weather_report,
        "mars_facts_html" : mars_facts_html,
        "hemisphere_list" : hemisphere_list
    }

    return mars_data












