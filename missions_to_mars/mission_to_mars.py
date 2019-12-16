#!/usr/bin/env python
# coding: utf-8


from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
import pandas as pd
import numpy as np




def init_browser():
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=True)

def scrape_data():
    
    browser = init_browser()

    nasa_url = 'https://mars.nasa.gov/news'


    time.sleep(3) #giving the browser enough time to open before accessing website to avoid an index error
    browser.visit(nasa_url)
    time.sleep(5)
    html = browser.html #if not enough time is given, the html of a blank webpage will be set to this variable
    soup = bs(html, 'html.parser')


    latest_news_paragraph = soup.find('div', class_='content_title')
    latest_news_paragraph = str(latest_news_paragraph)
    latest_news_paragraph = latest_news_paragraph.split('>')[2].split('</a')[0]
    latest_news_headline = soup.find('div', class_='article_teaser_body')
    latest_news_headline = str(latest_news_headline)
    latest_news_headline = latest_news_headline.split('>')[1].split('</')[0]
    #latest news headline and teaser paragraph



    jpl_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'

    browser.visit(jpl_url)
    html = browser.html
    soup = bs(html, 'html.parser')



    featured_image_url = soup.find('a', class_='button fancybox')
    featured_image_url = str(featured_image_url)
    featured_image_url = featured_image_url.split('data-fancybox-href="')[1].split('" d')[0]
    featured_image_url = f'https://www.jpl.nasa.gov{featured_image_url}' 
    #url of featured image


    twitter_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(twitter_url)


    html= browser.html
    soup = bs(html, 'html.parser')
    find_weather = soup.find_all('p', class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text')
    #get list of html of all tweets available by visiting the site


    first_forcast_index = len(find_weather) #set variable to the last tweet 
    for x in np.arange(0, len(find_weather)):
        not_weather_check = find_weather[x]
        not_weather_check = str(not_weather_check)
        not_weather_check = not_weather_check.split('pic.twitter')
        not_weather_check = len(not_weather_check)
        if not_weather_check == 2:
            if x < first_forcast_index:
                first_forcast_index = x
    latest_weather_tweet = find_weather[first_forcast_index]
    latest_weather_tweet = str(latest_weather_tweet)
    latest_weather_tweet = latest_weather_tweet.split('InSight ')[1].split('<')[0]
    #latest mars weather

    space_facts = 'https://space-facts.com/mars/'
    mars_list = pd.read_html(space_facts)


    df = mars_list[0]
    df.columns = ['Fact', 'Value']
    df = df.set_index('Fact')

    


    mars_facts_table = df.to_html()
    #html table of mars facts


    image_page = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(image_page)
    html = browser.html
    soup = bs(html, 'html.parser')

    locate_images = soup.find_all('div', class_='item')#[0].find_all('a')[0]


    list_of_images = [] #empty list for each image
    for x in np.arange(0,len(locate_images)):
        image =locate_images[x].find_all('a')[0]
        image = str(image)
        image = image.split('href="')[1].split('">')[0]
        image = f'https://astrogeology.usgs.gov{image}'
        browser.visit(image)
        html = browser.html
        soup = bs(html, 'html.parser')
        title = soup.find('h2', class_='title').text
        title = str(title)
        link = soup.find('div', class_='downloads').find('a')
        link = str(link)
        link = link.split('href="')[1].split('" ')[0]
        dictionary = {'title': title, 'link': link}
        list_of_images.append(dictionary)
    #dictionary of title and url of images
        


    browser.quit()
    #close browser when finished scraping

    #empty dictionary
    mars_data = {}
    #add scraped data to dictionary
    mars_data['headline'] = latest_news_headline
    mars_data['teaser_paragraph'] = latest_news_paragraph
    mars_data['weather'] = latest_weather_tweet
    mars_data['featured_image'] = featured_image_url
    mars_data['facts'] = mars_facts_table
    mars_data['images'] = list_of_images

    return mars_data



