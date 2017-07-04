

#Import Basics
import os
import re

#Import Matching
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

#Import Twitter
import tweepy #http://www.tweepy.org/
from tweepy import TweepError
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

#Import MongoDB
import json
from pymongo import MongoClient

#Import MediaWiki (MW)
import mwclient
from mwclient import Site #import mwclient

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


#Setup MongoDB
connection = c = MongoClient()
def connect_mongoDB():
    db = connection.Twitter #db.tweets.ensure_index("id", unique=True, dropDups=True)
    print("Mongo Twitter DB Connected")
    # The MongoDB connection info. Database name is Twitter and your collection name is politicians.
    #db.politicians.ensure_index( "id", unique=True, dropDups=True )
    db.politicians.create_index( "id", unique=True, dropDups=True )
    collection = db.politicians
    print("Collection politicians connected")
    # The MongoDB connection info. Database name is Twitter and your collection name is id_politicians.
    #db.id_politicians.ensure_index( "id", unique=True, dropDups=True )
    db.id_politicians.create_index( "id", unique=True, dropDups=True )
    id_collection = db.id_politicians
    print("Collection id_politicians connected")
    #### tweet_count = db.politicians.count("id", exists= True)
    #### print ("Total tweet count in DB is: " + str(tweet_count))
    #return(db, collection, id_collection)
    return(collection, id_collection)


database_connections = connect_mongoDB()
#db = database_connections[0]
collection = database_connections[0]
id_collection = database_connections[1]
#End MongoDB Setup


#Setup MediaWiki (MW)
with open(os.path.expanduser('~') + "/.invisible/mw.csv", 'r') as f:
    e = f.read()
    keys = e.split(',')
    print(keys)
    login_user = keys[0]  #consumer_key
    login_password = keys[1]  #consumer_secret


ua = 'CCWPTool run by User:1A' #UserAgent bot note
site = mwclient.Site(('http', 'www.climatepolitics.info'), path='/w/',)
site.login(login_user, login_password)
#End MW Setup




##### #### #### #### #### #### #### #### #### #### #### #### ####
#### Objective: Match and add twitter handles to MW profiles ####
#### #### #### #### #### #### #### #### #### #### #### #### #####
####
#### 1.  Reduce list2match to handles currently not in MW
#### 1A. Fetch all twitter handles in DB [db_handles_list]
#### 1B. Fetch all MW Handles [mw_handles_list]
#### 1C. Remove MW handles from the list of db_handles
####
#### 2.  Get string values for matching
#### 2A. From unassigned handles get handles DB name values
#### 2B. From page list get last name, first name, nickname
####
#### 3.  Calculate match confidence
####
#### 4.  Approve or reject matches


save_message = 'Matched twitter usernames to profiles and added handles (mw_valuesupdator_twitter_handles_matching_bot.py v01)'


####1.  Reduce list2match to handles currently not in MW
####1A. Fetch all twitter handles in DB [db_handles_list]
db_handles_list = []
returned = id_collection.find({"name":{"$exists":True}})
for dbitem in returned:
    db_handles_list.append(dbitem['screen_name'])


dbl = db_handles_list


#### 1B. Fetch all MW Handles [mw_handles_list]
#### 1B1. Get MW categories & their pages
#### 1B2. Get twitter handles from pages

#### 1B1. Get MW categories & their pages
#### Get list of categories to act on (#Uses http://www.climatecongress.info/wiki/BotResource:cats)
def get_cats_list():
    cat_list="BotResource:cats"
    catpage = site.Pages[cat_list]
    cats = catpage.text()
    return_list = cats.split("\n")
    return (return_list)


cat_list = get_cats_list()

page_list = []
for cat in cat_list:
  for a_page in site.Categories[cat]:
      listpage = site.Pages[a_page]
      page_list += [listpage.name]



#### 1B2. Get twitter handles from pages
mw_handles_list =[]
for page in page_list:
  one_page = site.Pages[page]
  page_text = one_page.text()
  #text = listpage.text()
  lines = page_text.split('\n')
  for line in lines:
    if line.startswith("|TW"):
      seg_line = line.split("/")
      for seg in seg_line:
        if re.match('\|TW|.*twitter\.com.*', seg):
          pass
        else:
          if seg == "":
            pass
          else:
            mw_handles_list.append(seg)
            print(seg)
    else:
      pass
      #print("pass")


mwl = mw_handles_list


#### 1C. Remove MW handles from the list of db_handles
print("MW list length " + str(len(mwl)))
print("DB list length " + str(len(dbl)))
new_list = [x for x in dbl if x not in mwl]
len(new_list)
print("Unique DB list length " + str(len(new_list)))

#### 2.  Get string values for comparison
#### 2A. From unassigned handles list get handles DB name values
DB_handles_names = []
for handle in new_list:
  matches = id_collection.find({"screen_name":handle})
  for match in matches:
    DB_handles_names.append(match['name'])


print("DB handles names length " + str(len(DB_handles_names)))

#### 2B. From page list get pagename, last name, first name, nickname

mw_handles_list =[]
for page in page_list:
  fname = ""
  nname = ""
  mname = ""
  lname = ""
  one_page = site.Pages[page]
  page_text = one_page.text()
  #text = listpage.text()
  lines = page_text.split('\n')
  MW_summary = []
  MW_name = []
  for line in lines:
    if line.startswith("|Firstname="):
      fname = line[11:]
      #MW_summary.append(fname)
      #print(fname)
    if line.startswith("|Nickname="):
      nname = line[10:]
      #MW_summary.append(nname)
      #print(nname)
    if line.startswith("|Middlename="):
      mname = line[12:]
      #MW_summary.append(mname)
      #print(mname)
    if line.startswith("|Lastname="):
      lname = line[10:]
      #MW_summary.append(lname)
      #print(lname)
    else:
      pass
  MW_summary.append(one_page.name)
  MW_summary.append(fname + " " + nname + " " + mname + " " + lname)
  mw_handles_list.append(MW_summary)


#mw_handles_list #mw_handles_list[items][0] is pagename, mw_handles_list[items][1] is first,middle,nick,lastname
mw_names = []
for one in mw_handles_list:
  mw_names.append(one[1])



#### Push twitter handle to MW profile (loop)
def add_handle_loop(t, page_name, dbmatch):
  text = site.Pages[page_name].text()
  if text.find("|TW1=") < 1:
    t = "|TW1="
    #print(t)
    text = text.replace("\n|Lastname=","\n" + t + "https://twitter.com/" + str(dbmatch['screen_name']) + "\n|Lastname=")
    #print(text)
    site.Pages[page_name].save(text, save_message)
    pass
  elif text.find("|TW2=") < 1:
    t = "|TW2="
    #print(t)
    text = text.replace("\n|Lastname=","\n" + t + "https://twitter.com/" + str(dbmatch['screen_name']) + "\n|Lastname=")
    #print(text)
    site.Pages[page_name].save(text, save_message)
    pass
  elif text.find("|TW3=") < 1:
    t = "|TW3="
    #print(t)
    text = text.replace("\n|Lastname=","\n" + t + "https://twitter.com/" + str(dbmatch['screen_name']) + "\n|Lastname=")
    #print(text)
    site.Pages[page_name].save(text, save_message)
    pass
  else:
    print("No free twitter handle values. Mannually resolve this")
    usertext = input("\n")


#### 3.  Calculate match confidence
for dbname in DB_handles_names:
  dbmatches = []
  page_name = ""
  #print(dbname + " " + str(process.extractOne(dbname, mw_names)))
  #print("Calculating")
  # https://pypi.python.org/pypi/fuzzywuzzy ## Varying match methods
  #eval = process.extractOne(dbname, mw_names)
  ## The token_ functions split the string on white-spaces, lowercase everything and get rid of non-alpha non-numeric characters, which means punctuation is ignored
  dbname_reduced = dbname.replace("Senator","").replace("Dr.","").replace("Judge.","").replace("President","").replace("Governor","")
  eval = process.extractOne(dbname_reduced_reduced, mw_names, scorer=fuzz.token_sort_ratio)
  confidence = eval[1]
  #### 4.  Approve or reject matches
  if confidence >= 85: #  More than 80, High confidence match
    #print("Match!  Twitter user name = MW profile name")
    print(dbname + " =" + str(eval[1]) + "= " + eval[0] + "   High confidence, more than 85")
    position = mw_names.index(eval[0])
    page_name = mw_handles_list[position][0]
    dbmatches = id_collection.find({"name":dbname})
    for dbmatch in dbmatches:
      print("https://twitter.com/" + str(dbmatch['screen_name']) + "    http://www.climatecongress.info/wiki/" + page_name)
      t = ""
      add_handle_loop(t, page_name, dbmatch)
      pass
  if confidence < 70: #  Less than 70, unlikely that there is a match
    #print ("The most likely MW profile is less than 70 match, no match is likely!")
    pass
elif confidence in range(70,85): # Match is in the 70-80 range you decide!
    print(dbname + " =" + str(eval[1]) + "= " + eval[0] )
    position = mw_names.index(eval[0])
    page_name = mw_handles_list[position][0]
    text = site.Pages[page_name].text()
    dbmatches = id_collection.find({"name":dbname})
    for dbmatch in dbmatches:
      print("https://twitter.com/" + str(dbmatch['screen_name']) + "    http://www.climatecongress.info/wiki/" + page_name)
      t = ""
      print("Uncertain 70-85 range. Visit users page. Is it a match y/n?")
      usertext = input("\n")
      if usertext == "y":
        print ("Match, adding handle to profile")
        add_handle_loop(t, page_name, dbmatch)
      else:
        print ("Not a match")
