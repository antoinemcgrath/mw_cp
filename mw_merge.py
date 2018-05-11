#!/usr/bin/python3
#MediaWiki
#Dir: /mnt/8TB/GITS/mw_cp/

import mwclient
import os
import difflib
import sys

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


def delete_page(a_del_page):
    a_del_page.delete()


def replace(a_del, a_keep):
    a_del = Politician(a_del)
    a_del.fetch_text()
    a_del_text = a_del.text
    a_del.parse(a_del_text)
    a_keep = Politician(a_keep)
    a_keep.fetch_text()
    a_keep_text = a_keep.text
    a_keep.parse(a_keep_text)
    return(a_del, a_keep)


def resolve(a, b):

    try:
        if a_del.Bioguide_id.lower() == a_keep.Bioguide_id.lower():
            pass
        else:
            print(a_del.Bioguide_id)
            print(a_keep.Bioguide_id)
    except AttributeError:
        pass

    try:
        if a_del.Q1.upper() == a_keep.Q1.upper():
            pass
        else:
            print(a_del.Q1)
            print(a_keep.Q1)
    except AttributeError:
        pass

    #try:
    #    if a_del.Q2.upper() == a_keep.Q2.upper():
    #        pass
    #    else:
    #        print(a_del.Q2)
    #        print(a_keep.Q2)
    #except AttributeError:
    #    pass

    try:
        if a_del.Q3.upper() == a_keep.Q3.upper():
            pass
        else:
            print(a_del.Q3)
            print(a_keep.Q3)
    except AttributeError:
        pass

    try:
        if a_del.FB1.upper() == a_keep.FB1.upper():
            pass
        else:
            print(a_del.FB1)
            print(a_keep.FB1)
    except AttributeError:
        pass

    try:
        if a_del.FB2.upper() == a_keep.FB2.upper():
            pass
        else:
            print(a_del.FB2)
            print(a_keep.FB2)
    except AttributeError:
        pass

    try:
        if a_del.TW1.upper() == a_keep.TW1.upper():
            pass
        else:
            print(a_del.TW1)
            print(a_keep.TW1)
    except AttributeError:
        pass

    try:
        if a_del.TW2.upper() == a_keep.TW2.upper():
            pass
        else:
            print(a_del.TW2)
            print(a_keep.TW2)
    except AttributeError:
        pass

    try:
        if a_del.Wiki1.upper() == a_keep.Wiki1.upper():
            pass
        else:
            print(a_del.Wiki1)
            print(a_keep.Wiki1)
    except AttributeError:
        pass

    try:
        if a_del.CampaignSite.upper() == a_keep.CampaignSite.upper():
            pass
        else:
            print(a_del.CampaignSite)
            print(a_keep.CampaignSite)
    except AttributeError:
        pass

    '''
    try:
        print(a_del.HouseOfficialSite, a_keep.HouseOfficialSite)
    except AttributeError:
        pass
    try:
        print(a_del.SenateeOfficialSite, a_keep.SenateeOfficialSite)
    except AttributeError:
        pass
    try:
        print(a_del.Thomas_id, a_keep.Thomas_id)
    except AttributeError:
        pass
    try:
        print(a_del.Facebook_Account, a_keep.Facebook_Account)
    except AttributeError:
        pass
    try:
        print(a_del.Facebook_id, a_keep.Facebook_id)
    except AttributeError:
        pass
    try:
        print(a_del.Twitter_Account, a_keep.Twitter_Account)
    except AttributeError:
        pass
    try:
        print(a_del.Google_Entity_id, a_keep.Google_Entity_id)
    except AttributeError:
        pass
    '''

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

wanted_variables = ["Bioguide_id", "Q1", "Q2", "Q3", "FB1",
                    "FB2", "TW1", "TW2", "Wiki1", "CampaignSite",
                    "HouseOfficialSite", "SenateeOfficialSite", "Thomas_id", "Facebook_Account",
                    "Facebook_id", "Twitter_Account", "Google_Entity_id"]



class Politician(object):
    'Common base class for every Politician'
    Politician = 0
    def __init__(self, name):
        self.name = name
    def fetch_text(self):
        self.text = site.pages.get(self.name).text()
        print("Text for %s returned" %(self.name))
    def parse(self, text):
        try:
            just_one = "Bioguide_id"
            instance = text.index(just_one)
            string = text[instance+len(just_one)+1:].split("|")[0]
            self.Bioguide_id = string
        except:
            pass
        try:
            just_one = "Q1"
            instance = text.index(just_one)
            string = text[instance+len(just_one)+1:].split("|")[0]
            self.Q1 = string
        except:
            pass
        try:
            just_one = "Q2"
            instance = text.index(just_one)
            string = text[instance+len(just_one)+1:].split("|")[0]
            self.Q2 = string
        except:
            pass
        try:
            just_one = "Q3"
            instance = text.index(just_one)
            string = text[instance+len(just_one)+1:].split("|")[0]
            self.Q3 = string
        except:
            pass
        try:
            just_one = "FB1"
            instance = text.index(just_one)
            string = text[instance+len(just_one)+1:].split("|")[0]
            self.FB1 = string
        except:
            pass
        try:
            just_one = "FB2"
            instance = text.index(just_one)
            string = text[instance+len(just_one)+1:].split("|")[0]
            self.FB2 = string
        except:
            pass
        try:
            just_one = "TW1"
            instance = text.index(just_one)
            string = text[instance + len(just_one) + 1:].split("|")[0]
            self.TW1 = string
        except:
            pass
        try:
            just_one = "TW1"
            instance = text.index(just_one)
            string = text[instance + len(just_one) + 1:].split("|")[0]
            self.TW1 = string
        except:
            pass
        try:
            just_one = "TW2"
            instance = text.index(just_one)
            string = text[instance + len(just_one) + 1:].split("|")[0]
            self.TW2 = string
        except:
            pass
        try:
            just_one = "Wiki1"
            instance = text.index(just_one)
            string = text[instance + len(just_one) + 1:].split("|")[0]
            self.Wiki1 = string
        except:
            pass
        try:
            just_one = "CampaignSite"
            instance = text.index(just_one)
            string = text[instance + len(just_one) + 1:].split("|")[0]
            self.CampaignSite = string
        except:
            pass
        try:
            just_one = "HouseOfficialSite"
            instance = text.index(just_one)
            string = text[instance + len(just_one) + 1:].split("|")[0]
            self.HouseOfficialSite = string
        except:
            pass
        try:
            just_one = "SenateeOfficialSite"
            instance = text.index(just_one)
            string = text[instance + len(just_one) + 1:].split("|")[0]
            self.SenateeOfficialSite = string
        except:
            pass
        try:
            just_one = "Thomas_id"
            instance = text.index(just_one)
            string = text[instance + len(just_one) + 1:].split("|")[0]
            self.Thomas_id = string
        except:
            pass
        try:
            just_one = "Facebook_Account"
            instance = text.index(just_one)
            string = text[instance + len(just_one) + 1:].split("|")[0]
            self.Facebook_Account = string
        except:
            pass
        try:
            just_one = "Facebook_id"
            instance = text.index(just_one)
            string = text[instance + len(just_one) + 1:].split("|")[0]
            self.Facebook_id = string
        except:
            pass
        try:
            just_one = "Twitter_Account"
            instance = text.index(just_one)
            string = text[instance + len(just_one) + 1:].split("|")[0]
            self.Twitter_Account = string
        except:
            pass
        try:
            just_one = "Google_Entity_id"
            instance = text.index(just_one)
            string = text[instance + len(just_one) + 1:].split("|")[0]
            self.Google_Entity_id = string
        except:
            pass
        print("Parsed %s " %self.name)


candidate_list = []
for a_page in site.Categories['Candidates']:
    listpage = site.Pages[a_page]
    candidate_list += [listpage.name]

elected_list = []

for a_cat in elected:
    for a_page in site.Categories[a_cat]:
        listpage = site.Pages[a_page]
        elected_list += [listpage.name]

a_elect_short = []
for a_elect in elected_list:
    a_elect_short.append(a_elect.split(' (')[0])

for a_short in a_elect_short:
    res = difflib.get_close_matches(a_short, candidate_list, 1)
    if len(res) > 0:
        spot = res[0]
        destination = elected_list[a_elect_short.index(a_short)]
        # Y/N Query are these to be merged
        prompt_text = str("Y to replace: \n" + spot + "\n" + destination)
        response = query_yes_no(prompt_text)
        if response == True:
            a_del = site.pages.get(spot)
            a_keep = site.pages.get(destination)

            a_del, a_keep = replace(a_del, a_keep)
            for one in wanted_variables:
                resolve(a_keep.one, a_del.one)

            # delete_page(a_del)
