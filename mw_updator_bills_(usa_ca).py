# MediaWiki
# python3 /Users/macbook/Documents/GITS/mediawiki/mw_usa_ca_bill_updater.py
# http://mwclient.readthedocs.io/en/latest/user/index.html

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

def bd_motion_votes_loop(vote):
    bd_motion_votes_text = "|bd_motion_votes_text=\n\n\n"
    for x in vote['votes']:
#        if "'committee'" in x and (x['committee']):
#            print(x['committee'])
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

        #Get no votes
        no = x['no_count']
        n_voters = x['no_votes']
        n_voters = (n_voters)
        n_vots = []
        for nv in n_voters:
            n_vots.append(nv['name'])
        #Get yes votes
        yes = x['yes_count']
        y_voters = x['yes_votes']
        y_voters = (y_voters)
        y_vots = []
        for yv in y_voters:
            y_vots.append(yv['name'])

        bd_motion_votes_text += ("\n\n'''On " + str(motion_date)  + " the " + chamber + " " + result + " the motion '" + motion + "' in a vote of Yea " + str(yes) + " to Nay " + str(no) + ".'''")
        if yes > 0:
            bd_motion_votes_text += ("\n\n*Voting 'Yea' there were " + str(yes) + " members: ")
            bd_motion_votes_text += ("'" + (str(y_vots)).replace(" '", " ").replace("',", ", ")[1:-1]+"'")
        if no > 0:
            bd_motion_votes_text += ("\n\n*Voting 'Nay' there were " + str(no) + " members: ")
            bd_motion_votes_text += ("'" + (str(n_vots)).replace(" '", " ").replace("',", ", ")[1:-1]+"'")
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








for a_page in site.Categories[SpecifiedCategory]:
    articlepage = site.Pages[a_page]
    profiletext = articlepage.text()
    val = str(articlepage.name.encode('utf-8'))
    print("Working on: " + val[2:] )

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
    val = val.split(" ")
    state = str(val[3][:-2]).lower()
    session = str(val[0])[2:6]+str(val[0])[7:]
    bill = str(val[1])[:2]+" "+str(val[1])[2:]

    # print (state + session + bill)
    # Input is expected to be formatted as ca20152016AB 197
    vote = openstates.bill_detail( state, session, bill)
    #print (bill)
    #print (vote['sponsors'])
    #    for x in vote:
    page_start = "{{US CA Bill\n"
    new_c = page_start
    new_c += custom
    new_c += ("|Instance of=Bill")
    new_c += ("\n|Session=" + str(session[:4])+"-"+session[4:])
    new_c += ("\n|Bill=" + str(bill))
    new_c += ("\n|Gov=USA CA")
    new_c += ("\n|Branch=Legislative")
    new_c += ("\n|OpenStateVoteID=" + vote['id'])
    new_c += ("\n|Bill page=" + str(vote['sources'][0])[9:-2])
    new_c += ("\n|Vote page=" + str(vote['sources'][0]).replace('billNavClient','billVotesClient')[9:-2])
    new_c += ("\n|JSON page="+ "https://openstates.org/api/v1/bills/" + state + "/" + session + "/" + bill + "/")
    #print("|Passed Senate=")
    #print("|Passed Assembly=")
    #print("|Crowdsourced name=")
    #print("|Crowdsourced description=")
    #print("|Crowdsourced detailed description=")
    new_c += ("\n|Official name=" + vote['title'])
    #new_c += ("\n|Official description=")
    new_c += ("\n|Official full description=" + vote['summary'])


    bd_final_actions_text = bd_final_actions_loop(vote)
    bd_final_actions_text += "\n<!--End_bd_final_actions-->"
    new_c += ("\n" +(bd_final_actions_text))

    bd_motion_votes_text = bd_motion_votes_loop(vote)
    bd_motion_votes_text += "\n<!--End_bd_motion_votes-->"
    new_c += ("\n" +(bd_motion_votes_text))

    page_end = "\n}}"
    new_c += page_end

    newtext = new_c
    #print (new_c)
    articlepage.save(newtext, 'Bill Updated (bill bot v01)')


    '''

        if x['yes_votes']['leg_id'] == 'CAL000494':
            print (x)

        upper_var = vote['votes'][0]
        for x in vote['votes']:
            if x['chamber'] == 'upper':
                if upper_var['date'] < x['date']:
                    upper_var = x

        lower_var = vote['votes'][0]
        for x in vote['votes']:
            if x['chamber'] == 'lower':
                if lower_var['date'] < x['date']:
                    lower_var = x


    list.append((vote['votes'][0]['chamber'])
    list.append(var['chamber'])




    datetime.datetime.strptime((x['date']), '%Y-%m-%d %H:%M:%S').date()
    (x['date']).datetime.strptime((x['date']), '%Y-%m-%d %H:%M:%S').date()
            print("Assembly motion: " + x['motion'])
            print("Assembly motion: " + x['motion'])



        if x['leg_id'] == caleg_id:
            print (x)
            if lower_var['date'] < x['date']:
                lower_var = x


    yes_votes no_votes other_votes

    vote['votes'][x]['motion']
    vote['votes'][4]['yes_votes']
    '''
