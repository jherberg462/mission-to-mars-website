# Mission to Mars Website

## Goals

In this project, I wanted to create a website that displays various up to date information about Mars from various sources. I also wanted the end-user to be able to cause the website application to obtain and display updated information.

## Flask App

I created a flask app that will connect to a MongoDB Database via pymongo outside of any routes. The flask app has a base route that queries the MongoDB Database, returns the render_template function that obtains an HTML template for the webpage, and inserts the returned data from the MongoDB query into the HTML template. The flask app also has a /scrape route that calls a function (described below in detail) that will scrape information from predefined sources, input this information into the MongoDB Database, and redirect the user back to the main route. 

## scrape_data function

I also created a function that will scrape specific information from two NASA websites, a twitter account that regularly tweets the current weather on Mars, a website that contains facts about Mars, and a USGS website. The function causes splinter to visit these websites, the HTML of the websites will be saved as a Beautiful Soup variable, and specific information within the Beautiful Soup variable will be saved as a new variable. All of the information I want to return is saved into a dictionary variable, and the dictionary is returned. 

## Deployment

To deploy the website, you need to run the app.py file in the missions_to_mars folder. Prior to running the app.py file, you need to change the URI variable on line 21 to a valid MongoDB URI. 
