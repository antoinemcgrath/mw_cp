# MediaWiki
# python3 /Users/macbook/Documents/GITS/mediawiki/mw_usa_ca_bill_updater.py
# http://mwclient.readthedocs.io/en/latest/user/index.html
# add bill info to wiki bot page
# openstates.org/api/v1/bills/ca/20152016/AB 1550/
# cat ~/.sunlight.key
import mwclient
from mwclient import Site
import re
import sunlight
from sunlight import openstates
import json
import csv
import datetime
from mwclient import Site #import mwclient
import os
from time import sleep


sub_category_current = "2017-2018"

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
catsig = "_(USA_CA)"
new_bill_text = "{{US CA Bill}}"
leg_list = "usa_ca_votes" ### Results in http://www.climatepolitics.info/wiki/BotResource:usa_ca_votes


def get_leg_item(leg_list): ### legislationtext = get_leg_item(leg_list) ###Returns a list of legislation
    legislationpage = "BotResource:"+leg_list ##This block fetches the legislation of interest
    print ("Queried MediaWiki for "+ legislationpage)
    legislation = site.pages[legislationpage]
    legislationtext = legislation.text()
    legislationtext = legislationtext.split('\n')
    #print (legislationtext)
    for line in legislationtext:
        #input ca,20172018,AB 151,
        #output 2017-2018_AB378_(USA_CA)
        data_legis = line.split(',')
        state = data_legis[0]
        session = data_legis[1]
        session = str(session[:4])+"-"+str(session[4:])
        bill = (data_legis[2]).replace(" ","")
        bill_page = (session+ "_"+bill+catsig)
        if len(site.pages[bill_page].text()) < 10:
            print("create page")
            site.pages[bill_page].save(new_bill_text, 'New bill page created (bill updator bot v01)')
            print(bill_page)
        else:
            print("Bill page exists: " + "www.climatepolitics.info/wiki/" + str(bill_page))
            #print(site.pages[legislation].text())




get_leg_item(leg_list) #print(legislationtext)






def bd_motion_votes_loop(vote):
    bd_motion_votes_text = "|bd_motion_votes_text=\n\n\n"
    for x in vote['votes']:
#        if "'committee'" in x and (x['committee']):
        #print(x['committee'])
#n_voters = x['committee']
#n_voters = (n_voters)
#n_vots = []
#for nv in n_voters:
#    n_vots.append(nv['name'])

#        else:
#            pass
        motion = x['motion']
        motion_date = x['date'][:-9]
        chamber = (str(x['chamber'])).replace("upper", "Senate").replace("lower", "Assembly")
        result = (str(x['passed'])).replace("True", "passed").replace("False", "did not pass")
        no = x['no_count']        #Get no votes
        n_voters = x['no_votes']
        n_voters = (n_voters)
        n_vots = []
        for nv in n_voters:
            n_vots.append(nv['name'])

        yes = x['yes_count']         #Get yes votes
        y_voters = x['yes_votes']
        y_voters = (y_voters)
        y_vots = []
        for yv in y_voters:
            y_vots.append(yv['name'])

        other = x['other_count']         #Get other votes
        o_voters = x['other_votes']
        o_voters = (o_voters)
        o_vots = []
        for ov in o_voters:
            o_vots.append(ov['name'])

        bd_motion_votes_text += ("\n\n'''On " + str(motion_date)  + " the " + chamber + " " + result + " the motion '" + motion + "' in a vote of Yea " + str(yes) + " to Nay " + str(no) + ".'''")
        if yes > 0:
            bd_motion_votes_text += ("\n\n*Voting 'Yea' there were " + str(yes) + " members: ")
            bd_motion_votes_text += ("'" + (str(y_vots)).replace(" '", " ").replace("',", ", ")[1:-1]+"'")
        if no > 0:
            bd_motion_votes_text += ("\n\n*Voting 'Nay' there were " + str(no) + " members: ")
            bd_motion_votes_text += ("'" + (str(n_vots)).replace(" '", " ").replace("',", ", ")[1:-1]+"'")
        if other > 0:
            bd_motion_votes_text += ("\n\n*Not voting there were " + str(other) + " members: ")
            bd_motion_votes_text += ("'" + (str(o_vots)).replace(" '", " ").replace("',", ", ")[1:-1]+"'")

    return (bd_motion_votes_text)





def bd_final_actions_loop(vote):
    bd_final_actions_text = '|bd_final_actions_text=\n\n\n<div style="background-color: #ddf5eb; border-style: dotted;">\n\n'
    if vote['action_dates']['passed_upper'] is not None:
        bd_final_actions_text += ("::*Final passing Senate vote: " + vote['action_dates']['passed_upper'][:-9]+"\n\n")
    else:
        pass
    if vote['action_dates']['passed_lower'] is not None:
        bd_final_actions_text += ("::*Final passing Assembly vote: " + vote['action_dates']['passed_lower'][:-9]+"\n\n")
    else:
        pass
    if vote['action_dates']['signed'] is not None:
        bd_final_actions_text += ("::*Signed by Governor: " + vote['action_dates']['signed'][:-9]+"\n\n")
    else:
        pass
    bd_final_actions_text += "</div>\n\n"
    return(bd_final_actions_text)




def get_vote_roles(vote):
    ## Get Legislation Role Value on Bill
    legislation_role = 0
    role = ""
    lead_authors = []
    coauthors = []
    for cs in vote['sponsors']:
        if cs['type'] != 'other':
            legislation_role = legislation_role+1
            role = (cs['type'])
            if role == 'sponsor':
                lead_authors.append(cs['name'])
                #lead_authors.append(cs['leg_id'])
            if role == 'primary':
                lead_authors.append(cs['name'])
                #lead_authors.append(cs['leg_id'])
            if role == 'cosponsor':
                coauthors.append(cs['name'])
                #coauthors.append(cs['leg_id'])
    uniq_lead_authors = set(lead_authors)
    uniq_coauthors = set(coauthors)
    #print (vote['title'])
    authors = ""
    coauthors = ""
    if len(uniq_lead_authors) != 0:
        authors += (str(uniq_lead_authors).replace("{'","").replace("'}","").replace(" '"," ").replace('{"','').replace('"}','').replace(' "',' ').replace('",',',').replace("',",","))
    if len(uniq_coauthors) != 0:
        coauthors += (str(uniq_coauthors).replace("{'","").replace("'}","").replace(" '"," ").replace('{"','').replace('"}','').replace(' "',' ').replace('",',',').replace("',",","))
            #[{'name': 'De León', 'official_type': 'LEAD_AUTHOR', 'leg_id': 'CAL000057', 'type': 'primary'}, {'name': 'Leno', 'official_type': 'LEAD_AUTHOR', 'leg_id': 'CAL000003', 'type': 'primary'}, {'name': 'Allen', 'official_type': 'COAUTHOR', 'leg_id': 'CAL000490', 'type': 'cosponsor'}, {'name': 'Hancock', 'official_type': 'COAUTHOR', 'leg_id': 'CAL000009', 'type': 'cosponsor'}, {'name': 'Monning', 'official_type': 'COAUTHOR', 'leg_id': 'CAL000107', 'type': 'cosponsor'}]
            #print(role)
            #print(vote['sponsors'])
            #print ("role" + str(bill))
    return(authors, coauthors)






for a_page in site.Categories[SpecifiedCategory]:
    articlepage = site.Pages[a_page]
    profiletext = articlepage.text()
    print(str(articlepage.name))
    val = str(articlepage.name.encode('utf-8'))
    print(val)
    if val.find('Bill') > 0:    # Skip pcategory pages that are not bills themselves (example US_CA_Bill which is an index page)
        print("Skipping what appears to be an index or other non bill profile page within the bill category")
        articlepage = ""
        print("Reset articlepage")
    #val = str(articlepage.name.encode('utf-8'))
    val = str(articlepage.name.encode('utf-8'))

    # Skip pcategory pages that are not bills themselves (example US_CA_Bill which is an index page)
    print(val)
    print(val.find('<Page object'))
    if val.find('<Page object') > 0:
        val = val.replace("<Page object 'b'","").replace("'' for <Site object '('http', 'www.climatepolitics.info')/w/'>>","")
        print (val)
    else:
        print(val)
        pass
    if val.find('Bill') > 0:
        pass
    else:
         val = val.replace('b"<Pag','').replace("e object '","").replace("' for <Site object '('http', 'www.climatepolitics.info')/w/;","").replace("' for <Sit('http', 'www.climatepolitics.info')/w/'","").replace('>>"','')


         #print("Working on: " + val[0:] )
         print("Working on: " + val[1:] )
         #print("Working on: " + val[2:] )
         #print("Working on: " + val[3:] )
         val = val[1:]
         #Get Custom values
         ends = [match.start() for match in re.finditer(re.escape("|"), profiletext)]
         moreends = [match.start() for match in re.finditer(re.escape("}"), profiletext)]
         allends = ends + moreends
         custs = [match.start() for match in re.finditer(re.escape("|Crowdsourced"), profiletext)]
         morecusts = [match.start() for match in re.finditer(re.escape("|Suggested"), profiletext)]
         allcusts = custs + morecusts
         matches = [item for item in allcusts if item in allends]
         indices = [allends.index(i) for i in matches]
         custom = ""
         for i in indices:
             custom += (profiletext[allends[i]:allends[i+1]])
         ##ADD custom back to page later


         #Get vote id values for Openstates query
         #print(val)
         val = val.split(" ")
         state = str(val[3][:-2]).lower()
         print(state)
         #session = str(val[0])[2:6]+str(val[0])[7:]
         #print(session)
         session = str(val[0])[1:5]+str(val[0])[6:]
         print(session)
         bill = str(val[1])[:2]+" "+str(val[1])[2:]
         print(bill)

         print("Forming API query akin to URL query: openstates.org/api/v1/bills/ca/20152016/AB 1550/")
         delay = (1.72)
         sleep(delay)
         print (state + session + bill)
         # Input is expected to be formatted as ca20152016AB 197
         vote = openstates.bill_detail(state, session, bill)
         #print (bill)
         #print (vote['sponsors'])
         #    for x in vote:
         page_start = "{{US CA Bill\n"
         new_c = page_start
         new_c += custom
         new_c += ("|Instance of=Bill")
         new_c += ("\n|Session=" + str(session[:4])+"-"+str(session[4:]))
         new_c += ("\n|Bill=" + str(bill))
         new_c += ("\n|Gov=USA CA")
         new_c += ("\n|Branch=Legislative")
         new_c += ("\n|OpenStateVoteID=" + vote['id'])
         new_c += ("\n|Bill page=" + str(vote['sources'][0])[9:-2])
         new_c += ("\n|Vote page=" + str(vote['sources'][0]).replace('billNavClient','billVotesClient')[9:-2])
         new_c += ("\n|JSON page=" + "https://openstates.org/api/v1/bills/" + state + "/" + session + "/" + bill + "/")
         #print("|Passed Senate=")
         #print("|Passed Assembly=")
         #print("|Crowdsourced name=")
         #print("|Crowdsourced description=")
         #print("|Crowdsourced detailed description=")
         new_c += ("\n|Official name=" + vote['title'])
         new_c += ("\n|Official description=")
         Roles = get_vote_roles(vote) #Authors/Coauthors
         if Roles[0] != 0:
             new_c += ("\n|Authors=" + str(Roles[0]))
         if Roles[1] != 0:
             new_c += ("\n|Coauthors=" + str(Roles[1]))


         bd_final_actions_text = bd_final_actions_loop(vote)
         bd_final_actions_text += "\n<!--End_bd_final_actions-->"
         new_c += ("\n" +(bd_final_actions_text))

         bd_motion_votes_text = bd_motion_votes_loop(vote)
         bd_motion_votes_text += "\n<!--End_bd_motion_votes-->"
         new_c += ("\n" +(bd_motion_votes_text))


         if sub_category_current == str(session[:4])+"-"+str(session[4:]):
             page_end = "[[Category:US_CA_Bill_Current]]"
         else:
             page_end = "[[Category:US_CA_Bill_Historical]]"
         page_end += "\n}}"
         new_c += page_end

         newtext = new_c

         #Drop any accidental extra spacing
         old_A = "\n\n\n"
         new_A = "\n\n"
         old_B = "\n|\n|\n|"
         new_B = "\n|\n|"
         newtext = newtext.replace(old_A,new_A).replace(old_B,new_B)
         newtext = newtext.replace(old_A,new_A).replace(old_B,new_B)
         newtext = newtext.replace(old_A,new_A).replace(old_B,new_B)
         #print (new_c)

         print(articlepage)

         try:  #Due to some page objects being returned within page objects for an unknown reeason
             (a_page).save(newtext, 'Bill Updated (bill bot v01)')
             articlepage = ""
             pass
             #print("Reset articlepage")
         except AttributeError:
             print("Exception: a_page doesn't exist")
