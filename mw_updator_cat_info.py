#!/usr/bin/python3
#### Summary: Handles updator
# Searches each category for new twitter handles
# Updates (category)_info page on MediaWiki
# ex. http://www.climatepolitics.info/wiki/US_CA_Assembly_info
# Updates twitter lists
# ex. https://twitter.com/AGreenDCBike/lists/us-ca-assembly
#Dir: /mnt/8TB/GITS/mw_cp/
#Execution schedule is every day at 2:30AM  ##crontab -e
##30 2 * * * /usr/bin/python3 /mnt/8TB/GITS/mw_cp/mw_updator_cat_info.py


import logging
#logging.basicConfig(filename='python_debug.log',level=logging.DEBUG) #Stores all runs
logging.basicConfig(filename='python_debug.log', filemode='w', level=logging.DEBUG) #Stores last run
#logging.debug('') #logging.info('') #logging.warning('')

import mwclient
import re
import os
import os.path
from pymongo import MongoClient
connection = c = MongoClient()

#Import Twitter
import tweepy #http://www.tweepy.org/


#Setup Twitter
#twitterKEYfile = os.path.expanduser('~') + "/.invisible/twitter01.csv" #
twitterKEYfile = os.path.expanduser('~') + "/.invisible/twitter02.csv" #AGreenDCBike
#twitterKEYfile = os.path.expanduser('~') + "/.invisible/twitter03.csv" #
#twitterKEYfile = os.path.expanduser('~') + "/.invisible/twitter05.csv" #

def get_twitter_keys(twitterKEYfile):
    #print("Loop3")
    with open(twitterKEYfile, 'r') as f:
        e = f.read()
        keys = e.split(',')
        consumer_key = keys[0]  #consumer_key
        consumer_secret = keys[1]  #consumer_secret
        access_key = keys[2]  #access_key
        access_secret = keys[3]  #access_secret
    # http://tweepy.readthedocs.org/en/v3.1.0/getting_started.html#api
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)
    return (api)

api = get_twitter_keys(twitterKEYfile)

#End Twitter Setup

####v01
edit_note = 'Updated rapid twitter content (mw_updator_cat_info.py bot v01)'

#### Fetch access values (must be username+password for a MW with bot/admin permissions)
with open(os.path.expanduser('~') + "/.invisible/mw.csv", 'r') as f:
    e = f.read()
    keys = e.split(',')
    logging.debug(keys)
    login_user = keys[0]  #consumer_key
    login_password = keys[1]  #consumer_secret


#### Set MW to access
ua = 'CCWPTool run by User:1A' #UserAgent bot note
site = mwclient.Site(('https', 'www.climatepolitics.info'), path='/w/',)
site.login(login_user, login_password)

#### MongoDB Login
db = connection.Twitter
db.politicians.create_index( "id", unique=True, dropDups=True )
collection = db.politicians
#tweet_count = db.politicians.count("id", exists= True)


#### Get list of categories to act on (#Uses http://www.climatecongress.info/wiki/BotResource:cats)
def get_cats_list():
    cat_list="BotResource:cats"
    catpage = site.Pages[cat_list]
    cats = catpage.text()
    return_list = cats.split("\n")
    return (return_list)
cat_list = get_cats_list()





#### For each Category make a list of pages
for cat in cat_list:
    profiles_scanned = 0
    profiles_with_handles = 0
    handles_in_cat = 0
    print (cat)
    cat_info_page = str(cat + "_info")
    print (cat_info_page)
    cat_info = []
    handles = []
#### For each page write contents to a .txt file
    for a_page in site.Categories[cat]:
        page_info = []
        profiles_scanned += 1
        listpage = site.Pages[a_page]
        text = listpage.text()
        reg_exp = '(?i)^.*twitter.com/'

        ####page_info.append(listpage.name)
        #print(page_info)

        if "|TW=" in text:
            text.index("|TW=")
            tw_strt = text.index("|TW=")
            linelength = text[tw_strt:].index("\n")
            tw_name = text[tw_strt+4:tw_strt+linelength]
            handle = re.sub(reg_exp, "", tw_name)
            handles.append(handle)
            handles_in_cat += 1
        if "|TW1=" in text:
            tw1_strt = text.index("|TW1=")
            linelength = text[tw1_strt:].index("\n")
            tw_name = text[tw1_strt+5:tw1_strt+linelength]
            handle = re.sub(reg_exp, "", tw_name)
            handles.append(handle)
            handles_in_cat += 1
        if "|TW2=" in text:
            tw2_strt = text.index("|TW2=")
            linelength = text[tw2_strt:].index("\n")
            tw_name = text[tw2_strt+5:tw2_strt+linelength]
            handle = re.sub(reg_exp, "", tw_name)
            handles.append(handle)
            handles_in_cat += 1
        if "|TW3=" in text:
            tw3_strt = text.index("|TW3=")
            linelength = text[tw3_strt:].index("\n")
            tw_name = text[tw3_strt+5:tw3_strt+linelength]
            handle = re.sub(reg_exp, "", tw_name)
            handles.append(handle)
            handles_in_cat += 1
        #print (handles)
    if handles != []:
        cat_info = page_info = handles
        #profiles_with_handles += 1
    else:
        pass
    # Save handles to MW pages
    cat_info_page_mwObj = site.Pages[cat_info_page]
    cat_info_page_mwObj.save(str(cat_info), edit_note)
    if cat.startswith("US_"):
        cat_State = cat[:5]
        cat_State_list = []
        cat_State_list.append(handles)

    print (str(cat) + " profiles scanned: " + str(profiles_scanned))
    print (str(cat) + " profiles with handles: " + str(profiles_with_handles))
    print (str(cat) + " total handles in category: " + str(handles_in_cat))
    tw_list_id = cat.lower().replace("_","-").replace(" ","-")
    print (tw_list_id)

    # Find existing twitter list, if error it does not exist (create it)
    try:
        api.get_list(slug=tw_list_id, owner_screen_name='@AGreenDCBike')
    except tweepy.error.TweepError as e:
        print ("Tweepy Error")
        print (e)
        tw_list_desc = "Twitter handle list of representatives " + cat + " for www.climatepolitics.info"
        api.create_list(name = tw_list_id, mode = "public", description = tw_list_desc)
        print("Creating Twitter list")

    for handle in handles:
        print(handle)
        ####user = api.get_user(screen_name = handle)
        ####handle_id = user.id
        ####print(handle_id)
        #api.add_list_member(slug=cat,id=handle_id,owner_screen_name='AGreedsdsdsdsnDCBike')
        #a_screen_name = str("@"+handle)
        try:
            api.add_list_member(screen_name=handle, slug=tw_list_id, owner_screen_name='AGreenDCBike')
        except tweepy.error.TweepError as e:
            print ("Tweepy Error")
            print (e)
            print("Failed to add user: " + handle + " to twitter list: " + tw_list_id)
            pass
