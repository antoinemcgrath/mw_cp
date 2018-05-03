#!/usr/bin/python3
#MediaWiki
#Dir: /mnt/8TB/GITS/mw_cp/
import mwclient
import os

count = 0

save_note = "Bot merging content from like profiles & deleting one"


with open(os.path.expanduser('~') + "/.invisible/mw.csv", 'r') as f:
    e = f.read()
    keys = e.split(',')
    print(keys)
    login_user = keys[0]  #consumer_key
    login_password = keys[1]  #consumer_secret



#### Set MW to access
ua = 'CCWPTool run by User:1A' #UserAgent bot note
site = mwclient.Site(('https', 'www.climatepolitics.info'), path='/w/',)
site.login(login_user, login_password)



#### Get list of categories to act on (#Uses http://www.climatecongress.info/wiki/BotResource:cats)
def get_cats_list():
    pagename="BotResource:cats"
    catpage = site.Pages[pagename]
    cats = catpage.text()
    return_list = cats.split("\n")
    return (return_list)


cat_list = get_cats_list()

new_list = []
newer_list = []
unique = []

for cat in cat_list:
    if cat.startswith("US_"):
        print (cat[0:5])
        newer_list.append(cat[0:5])
    else:
        pass