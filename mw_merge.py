#!/usr/bin/python3
#MediaWiki
#Dir: /mnt/8TB/GITS/mw_cp/
import mwclient
import os
import difflib
import sys
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






def query_yes_no(question, default=None):
    """Ask a yes/no question via raw_input() and return their answer.
    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).
    The "answer" return value is True for "yes" or False for "no".
    """
    valid = {"yes": True, "y": True, "ye": True,
             "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)
    while True:
        sys.stdout.write(question + prompt)
        choice = input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "
                             "(or 'y' or 'n').\n")



'''
Candidates
US_CA_Senate
US_CA_Bill
US_CA_Assembly
US-House
US-Senate‏‎
US TX House
US TX Senate
'''

cat_list = ['Candidates']
elected = ['US-House', 'US-Senate']
‏‎
candidate_list =[]
for a_page in site.Categories['Candidates']:
    listpage = site.Pages[a_page]
    candidate_list += [listpage.name]

elected_list =[]
for a_cat in elected:
    for a_page in site.Categories[a_cat]:
        listpage = site.Pages[a_page]
        elected_list += [listpage.name]

a_elect_short = []
for a_elect in elected_list:
    a_elect_short.append(a_elect.split(' (')[0])



for a_can in candidate_list:
    res = difflib.get_close_matches(a_can, a_elect_short, 1)
    if len(res) > 0:
        #print(a_can, res)
        spot = a_elect_short.index(res[0])
        prompt_text = str("Y to replace \n" + a_can + "\n" + elected_list[spot])
        response = query_yes_no(prompt_text)
        if response == True:
            a_del = site.pages.get(a_can)
            a_keep = site.pages.get(elected_list[spot])
            replace_loop(a_can, elected_list[spot])
            delete_loop(a_can)

