#MediaWiki
#python3 "/Users/macbook/Documents/GITS/mediawiki/mw_find&replace.py"
#find&replace bot v01
#https://mwclient.readthedocs.io/en/latest/reference/site.html?highlight=categories


import mwclient
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



old_A = "{{US CA Upper"
new_A = "{{US CA Senate"

old_B = "{{US CA Lower"
new_B = "{{US CA Assembly"

old_C = " yay "
new_C = " yea "

old_D = " Yay "
new_D = " Yea "

old_E = " yays "
new_E = " yeas "

old_F = " Yays "
new_F = " Yeas "

old_G = "Wing=Lower"
new_G = "Wing=Assembly"

old_H = "Wing=Upper"
new_H = "Wing=Senate"

for a_page in site.search('"USA CA"'):
    articlepage = a_page['title']
    articlepage = site.Pages[articlepage]
    profiletext = articlepage.text()
    print("Updated: " + str(articlepage.name.encode('utf-8')))
    newtext = (profiletext).replace(old_A,new_A).replace(old_B,new_B).replace(old_C,new_C).replace(old_D,new_D).replace(old_E,new_E).replace(old_F,new_F).replace(old_G,new_G).replace(old_H,new_H)
    #print(newtext.encode('utf-8'))
    articlepage.save(newtext, 'Replaced variants of Upper/Lower/Yay with Senate/Assembly/Yea (find&replace bot v01)')
    print("UPDATED!")
