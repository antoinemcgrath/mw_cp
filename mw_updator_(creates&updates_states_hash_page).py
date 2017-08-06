#!/usr/bin/python3
#MediaWiki
#Dir: /mnt/8TB/GITS/mw_cp/
#Output: /mnt/8TB/GITS/mw_cp/mw_site_backups/
#Execution schedule is Wednesdays at 1:30AM  ##crontab -e
##30 1 * * 3 /usr/bin/python3 /mnt/8TB/GITS/mw_cp/mw_updator_(creates&updates_states_hash_page).py
import logging
#logging.basicConfig(filename='python_debug.log',level=logging.DEBUG) #Stores all runs
logging.basicConfig(filename='python_debug.log', filemode='w', level=logging.DEBUG) #Stores last run
#logging.debug('')#logging.info('')#logging.warning('')
import mwclient
import os
import os.path

####v01
edit_note = 'Updates hash list for each state (mw_updator_(creates&updates_states_hash_page).py bot v01)'

standard_hashes = ["climate","carbon","globalwarming","global warming","renewable"]

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

new_list = []
newer_list = []
unique = []

for cat in cat_list:
    if cat.startswith("US_"):
        print (cat[0:5])
        newer_list.append(cat[0:5])
    else:
        pass


[unique.append(item) for item in newer_list if item not in unique]
print(unique)



for one in unique:
    bot_page = "BotResource:"+ one
    hashes = []
    bill_hashes = []
    a_botpage = site.Pages[bot_page]
    texts = a_botpage.text()
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
