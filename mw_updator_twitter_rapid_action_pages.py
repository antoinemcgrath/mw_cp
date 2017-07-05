#!/usr/bin/python3
#MediaWiki
#Dir: /mnt/8TB/GITS/mw_cp/
#Output: /mnt/8TB/GITS/mw_cp/mw_site_backups/
#Execution schedule is Wednesdays at 1:30AM  ##crontab -e
##30 1 * * 3 /usr/bin/python3 /mnt/8TB/GITS/mw_cp/mw_updator_twitter_rapid_action_pages.py

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
# The MongoDB connection info. This assumes your database name is Political and your collection name is tweets.
#connection = Connection('localhost', 27017)
db = connection.Twitter
db.politicians.create_index( "id", unique=True, dropDups=True )
collection = db.politicians




insert_start = "|STW=<!--StartSTW--> {{#widget:Tweet|id=794256025297653761}}\n"
insert_end = "<!--EndSTW-->\n"


####v01
edit_note = 'Updates each rapid action page (mw_updator_twitter_rapid_action_pages.py bot v01)'

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





#### Get list of categories to act on (#Uses http://www.climatecongress.info/wiki/BotResource:cats)
def get_cats_list():
    pagename="BotResource:cats"
    catpage = site.Pages[pagename]
    cats = catpage.text()
    return_list = cats.split("\n")
    return (return_list)


cat_list = get_cats_list()


# List of Categories # http://www.climatecongress.info/wiki/BotResource:cats
# Twitter list of cat members # https://twitter.com/AGreenDCBike/lists/us-ca-assembly
# Relevant hashes to cat # http://www.climatepolitics.info/wiki/BotResource:US_CA_Hashes
## Category users list # http://www.climatecongress.info/wiki/US_CA_Senate_info

#http://www.climatepolitics.info/wiki/US_CA_Senate_recent_activities

# Get cat.
# Addend _Recent_Actions  : cat +
# Get hashes of interest  : BotResource:US_CA_Hashes
# Get twitter list

def get_pages_loop(cat):
    action_page = cat + "_Recent_Actions"
    tw_list_id = cat.lower().replace("_","-").replace(" ","-")
    if cat.startswith("US_"):
        #print (cat[0:5])
        hashpagename="BotResource:" + (cat[0:5]) + "_Hashes"
        catpage = site.Pages[hashpagename]
        cats = catpage.text()
        return_list = cats.split("\n")
        return (cat,action_page,tw_list_id,hashpagename)
    else:
        pass


for cat in cat_list:
    returns = get_pages_loop(cat)
    if returns == None:
        #print ("Pass (None)")
        pass
    else:
        print (returns)
        cat = returns[0]
        action_page = returns[1]
        tw_list_id = returns[2]
        hashpagename = returns[3]
        catinfo = cat + "_info"
        #get hash list
        #get recent tweets
        #filter tweets
        #post to url

        a_tw_list_id_page = site.Pages[catinfo]
        tw_listtexts = a_tw_list_id_page.text()
        tw_list = ast.literal_eval(tw_listtexts)
        users_re = re.compile('|'.join(tw_list), re.IGNORECASE)

        a_botpage = site.Pages[hashpagename]
        hashtexts = a_botpage.text()
        hashes = ast.literal_eval(hashtexts)
        keywords_re = re.compile('|'.join(hashes), re.IGNORECASE)

        handle = "RepMikeQuigley"
        #handles_climate_tweets = 0
        #total_tws = str(db.politicians.find({"user.screen_name": handle}).count())
        #results = db.politicians.find({"user.screen_name": users_re, "text": keywords_re})
        #results = db.politicians.find({"user.screen_name": handle, "text": "climate"})
        results = db.politicians.find({"user.screen_name": handle, "text": keywords_re})
        print(results.count())
        #handles_climate_tweets += results.count()

'''

for hash in hashes:

    #print(texts)
    texts = texts.split("\n")
    for line in texts:
        bill = (line.split(","))[2]
        bill_hashes.append(bill)
        bill_hashes.append(bill.replace(" ","_"))
        bill_hashes.append(bill.replace(" ","-"))
        bill_hashes.append(bill.replace(" ",""))
    hashes.extend(bill_hashes)
    hashes.extend(standard_hashes)
    print(hashes)

    cat_hashes_url = bot_page + "_Hashes"
    cat_hashes_page = site.Pages[cat_hashes_url]
    cat_hashes_page.save(str(hashes), edit_note)
    print("Updated hash list: www.climatepolitics.info/wiki/" + cat_hashes_url)
'''
