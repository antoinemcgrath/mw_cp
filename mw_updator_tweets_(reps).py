#!/usr/bin/python3
#MediaWiki
#Dir: /mnt/8TB/GITS/mw_cp/
#Output: /mnt/8TB/GITS/mw_cp/mw_site_backups/
#Execution schedule is Wednesdays at 1:30AM  ##crontab -e
##30 1 * * 3 /usr/bin/python3 /mnt/8TB/GITS/mw_cp/mw_creation_of_site_backups.py

import mwclient
import re
import os
import os.path
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
edit_note = 'Updated twitter content (mw_updator_tweets_(reps).py bot v01)'
insert_start = "|STW=<!--StartSTW--> {{#widget:Tweet|id=794256025297653761}}\n"
insert_end = "<!--EndSTW-->\n"

#### Fetch access values (must be username+password for a MW with bot/admin permissions)
with open(os.path.expanduser('~') + "/.invisible/mw.csv", 'r') as f:
    e = f.read()
    keys = e.split(',')
    #print(keys)
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
#print ("DB:Twitter Collection:political tweets count is : " + str(tweet_count))


#### Get list of categories to act on (#Uses http://www.climatecongress.info/wiki/BotResource:cats)
def get_cats_list():
    cat_list="BotResource:cats"
    catpage = site.Pages[cat_list]
    cats = catpage.text()
    return_list = cats.split("\n")
    return (return_list)


cat_list = get_cats_list()




def get_atweet_embed(obj):
    a_ = '<blockquote class="twitter-tweet" data-lang="en"><p lang="en" dir="ltr">'
    b_atweet_text = str(obj["text"])
    #c_ = ' <a href="'
    #d_atweet_url = "pass"#str(obj["url"])
    #e_ = '">'
    f_  = '</p>'  #&mdash; '
    #g_name = str(obj["user"]["name"])
    #h_ = ' (@'
    i_atweet_user = str(obj["user"]["name"])
    #j_ = ')
    j_ ='<a href="https://twitter.com/'
    k_ = str(obj["user"]["screen_name"])
    l_ = '/status/'
    k_atweetid = str(obj["id_str"])
    #l_ = '">"'
    m_date = str(obj["created_at"]) #Formated as Month date, Year example:February 2, 2017
    o_ = '</a></blockquote>\n'
    #atweet = a_ + b_atweet_text + c_ + d_atweet_url + e_ + f_ + g_name + h_ + i_atweet_user + j_ + k_ + l_ + k_atweetid + l_ + m_date + o_
    atweet = a_ + b_atweet_text + f_ + j_ + k_ + l_ + k_atweetid + l_ + m_date + o_
    return(atweet)


#atweet = get_atweet_embed(obj)


######## DB queries
#### Works in terminal
#db.politicians.findOne()
#db.politicians.count({'id': {'$exists': true}},{})
#db.politicians.find({'user': {'$exists': true}},{"id": 1, "text": 1, "user.screen_name": 1, "created_at": 1, "_id":0})
#### Working test in py
#collection.count({"user.screen_name": handle})

def get_tweets_from_handle(handle, total_climate_tweets, insert_body):
    handles_climate_tweets = 0
    keywords_re = re.compile(r'climate|carbon|globalwarming|global warming|renewable', re.IGNORECASE)
    results = db.politicians.find({"user.screen_name": handle, "text": keywords_re})
    handles_climate_tweets += results.count()
    total_climate_tweets += handles_climate_tweets
    if handles_climate_tweets > 0:
        print("Twitter handle " + handle + " has " + str(handles_climate_tweets) + " 'climate' tweets.")
    else:
        pass
    for obj in results:
        #print (obj)
        atweet = get_atweet_embed(obj)
        insert_body += atweet
        #print(atweet)
        #print ("Text    " + str(obj["text"]))
        #print ("Date    " + str(obj["created_at"]))
    return (total_climate_tweets, insert_body)

def get_STW_insert(handles,total_handles):
    STW_insert = ""
    insert_body = ""
    insert_start = "|STW=<!--StartSTW-->'''Automatically captured tweets'''{{#widget:Tweet|id=794256025297653761}}\n"
    insert_end = "<!--EndSTW-->"
    STW_insert += insert_start
    for handle in handles:
        #print (handle)
        total_handles += 1
        total_climate_tweets = 0
        tweets_from_handle = get_tweets_from_handle(handle,total_climate_tweets, insert_body)
        insert_body = tweets_from_handle[1]
       # print ("The current count of climate tweets is " + str(tweets_from_handle[0]))
    #print(insert_body)
    #print(type(insert_body))
    #### The following section takes insert_body (the new string of tweets to be embedded) and changes the order
    #### The order is changed by replacing irregularities, creating a list, prefacing each item in the list with a parsed date from a later portion of the item, reorder the list and then removing the preface and exporting back to a string
    #### new tweet(s) = newt(s)
    ib = insert_body.replace("</blockquote> ","</blockquote>")
    junk = re.split("(<blockquote class|<impossible123)", ib)
    junk = junk[1:]
    list_embed = [i1 + i2 for i1, i2 in zip(junk[0::2], junk[1::2])]
    sorted_tweets = ""
    newts = []
    for tweet in list_embed:
        #print(tweet[-44:-18])#Aug 10 21:47:18 +0000 2015 = MMM dd HH:mm:ss Z yyyy
        #print(str(parse(tweet[-44:-18])))
        newt = (str(parse(tweet[-44:-18]))) + (tweet)
        #print(newt)
        newts.append(newt)
    newts.sort(reverse=True)
    for sorted_tweet in newts:
        sorted_tweets += sorted_tweet[25:]
    #print(sorted_tweets)
    #print(type(sorted_tweets))

    STW_insert += sorted_tweets

    STW_insert += insert_end
    #print(STW_insert)
    #print(len(STW_insert))

    #print(str(type(insert_body)) + "is the type of the object insert_body")
    #print(str(type(STW_insert)) + "is the type of the object STW_insert")
    return (STW_insert)

#### For each Category make a list of pages
for cat in cat_list:
#### For each page write contents to a .txt file
    for a_page in site.Categories[cat]:
        profiles_scanned += 1
        listpage = site.Pages[a_page]
       # print (listpage.name)
        text = listpage.text()
        #(?i)^ means case insensitive
        handles = []
        reg_exp = '(?i)^.*twitter.com/'

        if "|TW=" in text:
            text.index("|TW=")
            tw_strt = text.index("|TW=")
            linelength = text[tw_strt:].index("\n")
            tw_name = text[tw_strt+4:tw_strt+linelength]
            handle = re.sub(reg_exp, "", tw_name)
            handles.append(handle)
        if "|TW1=" in text:
            tw1_strt = text.index("|TW1=")
            linelength = text[tw1_strt:].index("\n")
            tw_name = text[tw1_strt+5:tw1_strt+linelength]
            handle = re.sub(reg_exp, "", tw_name)
            handles.append(handle)
        if "|TW2=" in text:
            tw2_strt = text.index("|TW2=")
            linelength = text[tw2_strt:].index("\n")
            tw_name = text[tw2_strt+5:tw2_strt+linelength]
            handle = re.sub(reg_exp, "", tw_name)
            handles.append(handle)
        if "|TW3=" in text:
            tw3_strt = text.index("|TW3=")
            linelength = text[tw3_strt:].index("\n")
            tw_name = text[tw3_strt+5:tw3_strt+linelength]
            handle = re.sub(reg_exp, "", tw_name)
            handles.append(handle)

        if handles != []:
            #print (handles)
            profiles_with_handles += 1
            STW_insert = get_STW_insert(handles, total_handles)

            if len(STW_insert) > 110: # Normal (no change) is 109
                #print(len(STW_insert))
                #STW_lines_regex = '(?s) \|STW=<!--StartSTW-->.*<!--EndSTW-->'
                #STW_lines_regex = '\|STW=<!--StartSTW-->.*<!--EndSTW-->'
                STW_lines_regex = '\|STW=<!--StartSTW-->.*(?s)<!--EndSTW-->'
                if re.search("<!--StartSTW-->", text) == None:
                     #print("SHOULD INSERT NEW TWEET SECTION")
                     insert_here =  text.rfind("}}")    ####rfind finds in reverse
                     newtext = text[:insert_here] + STW_insert + text[insert_here:]
                else:
                     #print("SHOULD EDIT EXISTING TWEET SECTION")
                     #print(STW_lines_regex)
                     #print(STW_insert)
                     #print(text)
                     #print ("We found that the page had tweets already and will replace them")
                     newtext = re.sub(STW_lines_regex, STW_insert, text)
                     #print()
                     #print()
                     #print(newtext)
               #print(newtext)

                #Drop any accidental extra spacing
                old_A = "\n\n\n"
                new_A = "\n\n"
                old_B = "\n|\n|\n|"
                new_B = "\n|\n|"
                newtext = newtext.replace(old_A,new_A).replace(old_B,new_B)
                newtext = newtext.replace(old_A,new_A).replace(old_B,new_B)
                newtext = newtext.replace(old_A,new_A).replace(old_B,new_B)
                a_page.save(newtext, edit_note)
                #print("UPDATED!")

        else:
            pass


print ("Profiles scanned: " + str(profiles_scanned))
print ("Profiles with handles: " + str(profiles_with_handles))
print ("Total number of twitter handles: " + str(total_handles))
print ("Total number of climate tweets: " + str(total_climate_tweets))
