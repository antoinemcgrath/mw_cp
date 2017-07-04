#!/usr/bin/python3
#MediaWiki
#Dir: /mnt/8TB/GITS/mw_cp/
#Output: /mnt/8TB/GITS/mw_cp/mw_site_backups/
#Execution schedule is Wednesdays at 1:30AM  ##crontab -e
##30 1 * * 3 /usr/bin/python3 /mnt/8TB/GITS/mw_cp/mw_creation_of_site_backups.py
import logging
#logging.basicConfig(filename='python_debug.log',level=logging.DEBUG) #Stores all runs
logging.basicConfig(filename='python_debug.log', filemode='w', level=logging.DEBUG) #Stores last run
#logging.debug('')#logging.info('')#logging.warning('')
import mwclient
import re
import os
import os.path
import ast
import errno
import datetime
from dateutil.parser import *
from mwclient import Site #import mwclient
from pymongo import MongoClient
connection = c = MongoClient()



profiles_scanned = 0
profiles_with_handles = 0
total_handles = 0
total_climate_tweets = 0

####v01
edit_note = 'Updated rapid twitter content (mw_updator_tweets_(rapido).py bot v01)'

insert_start = "|STW=<!--StartSTW--> {{#widget:Tweet|id=794256025297653761}}\n"
insert_end = "<!--EndSTW-->\n"

#### Fetch access values (must be username+password for a MW with bot/admin permissions)
with open(os.path.expanduser('~') + "/.invisible/mw.csv", 'r') as f:
    e = f.read()
    keys = e.split(',')
    logging.debug(keys)
    login_user = keys[0]  #consumer_key
    login_password = keys[1]  #consumer_secret


#### Set MW to access
ua = 'CCWPTool run by User:1A' #UserAgent bot note
site = mwclient.Site(('http', 'www.climatepolitics.info'), path='/w/',)
site.login(login_user, login_password)

#### MongoDB Login
db = connection.Twitter
db.politicians.create_index( "id", unique=True, dropDups=True )
collection = db.politicians
#tweet_count = db.politicians.count("id", exists= True)


#### Get list of categories to act on (#Uses http://www.climatecongress.info/wiki/BotResource:cats)
def get_cats_list():
    pagename="BotResource:cats"
    catpage = site.Pages[pagename]
    cats = catpage.text()
    return_list = cats.split("\n")
    return (return_list)



cat_list = get_cats_list()


#### Get list of categories to act on (#Uses http://www.climatecongress.info/wiki/BotResource:cats)
def get_cat_info_list(cat):
    infopagename = str(cat + "_info")
    print (infopagename)
    infopage = site.Pages[infopagename]
    #print(infopage)
    catinfo = infopage.text()
    #print(catinfo)
    return_info = catinfo
    return (return_info)
#cat_info_list = get_cat_info_list()

for cat in cat_list:
    cat_info_list = get_cat_info_list(cat)
    iterables = ast.literal_eval(cat_info_list) #https://stackoverflow.com/questions/10775894/converting-a-string-representation-of-a-list-into-an-actual-list-object
    for profile in iterables:
        print(profile)
        print("printed profile")
        for handles in profile:
            print(handles)
            print("printed handles")
            #for handle in handles:
                #print(handle)
                #print("printed handle")

#Import Twitter
import tweepy #http://www.tweepy.org/
from tweepy import TweepError
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
