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
import datetime, pymongo
#from dateutil.parser import *
from mwclient import Site #import mwclient
from pymongo import MongoClient
connection = c = MongoClient()
# The MongoDB connection info. This assumes your database name is Political and your collection name is tweets.
#connection = Connection('localhost', 27017)
db = connection.Twitter
db.politicians.create_index("id", unique=True, dropDups=True )
db.politicians.create_index("user.screen_name")
db.politicians.create_index("text")
db.politicians.create_index("created_at")
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

#http://www.climatepolitics.info/wiki/US_CA_Senate_Recent_Actions

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
    atweet = a_ + b_atweet_text + f_ + j_ + k_ + l_ + k_atweetid + l_ + " " + m_date + o_
    return(atweet)


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

        action_page = site.Pages[action_page]
        a_pagetexts = action_page.text()


        a_tw_list_id_page = site.Pages[catinfo]
        tw_listtexts = a_tw_list_id_page.text()
        tw_list = ast.literal_eval(tw_listtexts)
        users_re = re.compile('|'.join(tw_list), re.IGNORECASE)

        a_botpage = site.Pages[hashpagename]
        hashtexts = a_botpage.text()
        hashes = ast.literal_eval(hashtexts)
        if len(tw_list) < 2:
            pass
        elif len(hashes) < 2:
            pass
        else:
            STW_insert = ""
            insert_body = ""
            keywords_re = re.compile('|'.join(hashes), re.IGNORECASE)
            handle = "RepMikeQuigley" #Test value
            #handles_climate_tweets = 0
            #total_tws = str(db.politicians.find({"user.screen_name": handle}).count())

            #start = datetime(2017, 2, 1, 18, 33, 46, 266943)
            #end = datetime.now()
            #print(start)
            #print(end)
            #db.posts.find({created_on: {$gte: start, $lt: end}});

            from bson.objectid import ObjectId
            gen_time = datetime.datetime(2017, 6, 20)
            dummy_id = ObjectId.from_datetime(gen_time)
            print(dummy_id)      #Test value   #59349f000000000000000000   #467280209323241472
            result = db.politicians.find({"_id": {"$gt": dummy_id}, "user.screen_name": users_re, "text": keywords_re}).sort("created_at")
            ##result = db.politicians.find({"user.screen_name": users_re, "text": keywords_re}).sort("created_at")
            #thirty_days_ago = datetime.datetime.utcnow() - datetime.timedelta(days=90)
            #print(thirty_days_ago)
            ###results = db.politicians.find({"user.screen_name": users_re, "text": keywords_re})
            ##results = db.politicians.find({"user.screen_name": handle, "text": "climate"})
            #results = db.politicians.find({ 'created_at': { '$gte': thirty_days_ago}})
            ##results = db.politicians.find({'created_at': {'$gte': start, '$lt': end}, "user.screen_name": handle, "text": keywords_re})
            ###results = db.politicians.find({"user.screen_name": handle, "text": keywords_re})
            countresult = result.count()
            #print(countresults)
            ##handles_climate_tweets += results.count()

            if countresult > 0:
                print("Handles in category " + str(cat) + " have " + str(countresult) + " tweets.")
            else:
                pass
            for obj in result:
                #print (obj)
                #atweet = get_atweet_embed(obj)
                #insert_body += atweet
                #print(atweet)
                #print ("Text    " + str(obj["text"]))
                ##print ("Tweet ID    " + str(obj["id_str"]) + "   Date    " + str(obj["created_at"]) )
                get_atweet_embed(obj)
                insert_body += atweet
            #return (total_climate_tweets, insert_body)


            insert_start = "|STW=<!--StartSTW-->'''Automatically captured tweets'''{{#widget:Tweet|id=794256025297653761}}\n"
            insert_end = "<!--EndSTW-->"
            STW_insert += insert_start
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
            ##return (STW_insert, total_climate_tweets)



            STW_lines_regex = '\|STW=<!--StartSTW-->.*(?s)<!--EndSTW-->'
            if re.search("<!--StartSTW-->", a_pagetexts) == None:
                #print("SHOULD INSERT NEW TWEET SECTION")
                insert_here =  a_pagetexts.rfind("}}")    ####rfind finds in reverse
                newtext = a_pagetexts[:insert_here] + STW_insert + a_pagetexts[insert_here:]
            else:
                #print("SHOULD EDIT EXISTING TWEET SECTION")
                #print(STW_lines_regex)
                #print(STW_insert)
                #print(text)
                #print ("We found that the page had tweets already and will replace them")
                newtext = re.sub(STW_lines_regex, STW_insert, a_pagetexts)
                ##Remove excess lines
            old_A = "\n\n\n"
            new_A = "\n\n"
            old_B = "\n|\n|\n|"
            new_B = "\n|\n|"
            newtext = newtext.replace(old_A,new_A).replace(old_B,new_B)
            newtext = newtext.replace(old_A,new_A).replace(old_B,new_B)
            newtext = newtext.replace(old_A,new_A).replace(old_B,new_B)
            a_page.save(newtext, edit_note)
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
