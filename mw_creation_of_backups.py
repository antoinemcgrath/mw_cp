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
import os
import errno
import datetime
from mwclient import Site #import mwclient

DATE = datetime.datetime.now().strftime('%Y-%m-%d')
base_dir = '/mnt/8TB/GITS/mw_cp/mw_site_backups/'+DATE+"/"


#### Fetch access values (must be username+password for a MW with bot/admin permissions)
with open(os.path.expanduser('~') + "/.invisible/mw.csv", 'r') as f:
    e = f.read()
    keys = e.split(',')
    print(keys)
    login_user = keys[0]  #consumer_key
    login_password = keys[1]  #consumer_secret


#### Set MW to access
ua = 'CCWPTool run by User:1A' #UserAgent bot note
site = mwclient.Site(('http', 'www.climatepolitics.info'), path='/w/',)
site.login(login_user, login_password)


#### Get list of categories to act on (#Uses http://www.climatecongress.info/wiki/BotResource:cats)
def get_cats_list():
    cat_list="BotResource:cats"
    catpage = site.Pages[cat_list]
    cats = catpage.text()
    return_list = cats.split("\n")
    return (return_list)
cat_list = get_cats_list()


#### Create directories when they do not exist
def make_path_exist(path):
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise
make_path_exist(base_dir)

#### For each Category make a list of pages
for cat in cat_list:
    make_path_exist(base_dir+cat)
#### For each page write contents to a .txt file
    for a_page in site.Categories[cat]:
        listpage = site.Pages[a_page]
        #print (listpage.name)
        text = listpage.text()
        f = open(os.path.join(base_dir+cat,listpage.name + ".txt"), "w")
        f.write(text)
        f.close()
