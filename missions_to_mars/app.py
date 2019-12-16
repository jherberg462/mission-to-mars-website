#!/usr/bin/env python
# coding: utf-8

# In[1]:


#Import Dependencies
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import pymongo
from mission_to_mars import scrape_data
import warnings 
warnings.filterwarnings("ignore")


# In[2]:


#set uri of mongo db
#I used an 'always free' azure db, so I updated the variable to x on the version uploaded to github
uri = 'x'
client = pymongo.MongoClient(uri)


# In[3]:


#!which chromedriver


# In[5]:


#Create Instance of Flask App
app = Flask(__name__)


# In[6]:


@app.route("/")
def index():
    #return one document from 'mars' db
    data = client.db.mars.find_one()

    # the mars data gets input into the index.html template
    return render_template("index.html", mars_data=data)


# In[ ]:


@app.route("/scrape")
def scraper():
    # create a mars collection
    mars = client.db.mars
    
    #calls scrape_date() function and assigns the dictionary it returned to the variable updating_data
    updating_data = scrape_data()#mission_to_mars.scrape()

    # updates database with dictionary in above variable
    mars.update({}, updating_data, upsert=True)

    # sends user back to '/'page.
    return redirect("/", code=302)


# In[ ]:


#set debug to True for troubleshooting, keep troubleshooting code out of production
if __name__ == '__main__':
    app.run(debug=False)

