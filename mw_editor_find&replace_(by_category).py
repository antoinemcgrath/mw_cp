#MediaWiki
# python3 "/Users/macbook/Documents/GITS/mediawiki/mw_find&replace_CategoryMethod.py"
# find&replace bot v01
# https://mwclient.readthedocs.io/en/latest/reference/site.html?highlight=categories

#/Users/macbook/.invisible

import re
import csv
import json
import datetime
import mwclient
from mwclient import Site #import mwclient
import os

#### Access your MW with bot/admin approved permissions
with open(os.path.expanduser('~') + "/.invisible/mw.csv", 'r') as f:
    e = f.read()
    keys = e.split(',')
    print(keys)
    login_user = keys[0]  #consumer_key
    login_password = keys[1]  #consumer_secret

ua = 'CCWPTool run by User:1A' #UserAgent bot note
site = mwclient.Site(('http', 'www.climatepolitics.info'), path='/w/',)
site.login(login_user, login_password)

SpecifiedCategory="US_CA_Bill"


old_A = "\n\n\n"
new_A = "\n\n"

old_B = "\n|\n|\n|"
new_B = "\n|\n|"

for a_page in site.Categories[SpecifiedCategory]:
    articlepage = site.Pages[a_page]
#for a_page in site.search('" (USA CA)"'):
#    print (a_page)
    #articlepage = a_page['title']
    #articlepage = site.Pages[articlepage]
    profiletext = articlepage.text()
    print("Updated: " + str(articlepage.name.encode('utf-8')))
    newtext = (profiletext).replace(old_A,new_A).replace(old_B,new_B)
    newtext = newtext.replace(old_A,new_A).replace(old_B,new_B)
    newtext = newtext.replace(old_A,new_A).replace(old_B,new_B)
    newtext = newtext.replace(old_A,new_A).replace(old_B,new_B)
    newtext = newtext.replace(old_A,new_A).replace(old_B,new_B)
    newtext = newtext.replace(old_A,new_A).replace(old_B,new_B)



    #print(newtext.encode('utf-8'))
    articlepage.save(newtext, 'Set colo & formatting of: This legislator is new to their position.... (find&replace bot v01)')
    print("UPDATED!")
