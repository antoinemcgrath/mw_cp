#!/usr/bin/python3
#MediaWiki
#Dir: /mnt/8TB/GITS/mw_cp/
import mwclient
import os

count = 0

save_note = "Bot restoring 2016 Candidate pages (that lost)"


#### directory to be restored
path = os.path.expanduser('~') + '/Documents/GITS/mw_cp/mw_site_backups/2017-03-09/Candidates'

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


#### Discover each file in the directory
for item in os.listdir(path):
    newItem = os.path.join(path, item)
    #### Copy content from file
    with open(newItem, 'r') as f:
        text = f.read()
        #### Insert text to new or existing MW page that has the same name as each file
        a_page = site.Pages[item[:-4]]
        a_page.save(text, save_note)
        count = count +1
        #print(text)
        #print(item)
        print (count)
