#MediaWiki
#python3

#Replace all spaces  in the delete_me.txt
#while read line; do python3 "/Users/macbook/Documents/GITS/mediawiki/mw_delete_pages_(from_a_list).py" $line; done < /Users/macbook/Documents/GITS/mediawiki/deletelist.txt

import mwclient
import sys
import os

#### Access your MW with bot/admin approved permissions
with open(os.path.expanduser('~') + "/.invisible/mw.csv", 'r') as f:
    e = f.read()
    keys = e.split(',')
    print(keys)
    login_user = keys[0]  #consumer_key
    login_password = keys[1]  #consumer_secret

ua = 'CCWPTool run by User:1A' #UserAgent bot note
site = mwclient.Site(('https', 'www.climatepolitics.info'), path='/w/',)
site.login(login_user, login_password)


if (len(sys.argv) != 2):
   print ("Please supply only one argument -- the URL to download")
   print (sys.argv)
   sys.exit(-1)



pagename = sys.argv[1]
print(pagename)

page = site.Pages[pagename]
page.delete(reason='US Congressional Candidate was not elected in 2016', watch=True)
print ("Deleted")
