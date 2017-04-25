#!/usr/bin/python3

# MediaWiki
# Requires ~/.sunlight.key

# cd /Users/macbook/Documents/GITS/mediawiki/
# python3 /Users/macbook/Documents/GITS/mediawiki/mw_usa_ca_votes_updator.py
# python3 /home/comp/Desktop/Climate_Politics/mediawiki/mw_usa_ca_votes_updator.py



#http://mwclient.readthedocs.io/en/latest/user/index.html

##Propublica API key
#curl "https://api.propublica.org/congress/v1/114/house/members.json" -H "X-API-Key: keykeykey"

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

Specified_A_Category = 'US_CA_Senate'
Specified_B_Category = 'US_CA_Assembly'

#http://www.climatecongress.info/wiki/Category:US_CA_Senate
#http://www.climatecongress.info/wiki/Category:US_CA_Assembly


#http://www.climatecongress.info/wiki/BotResource:usa_congress_votes
#leg_list = "usa_congress_votes"

#http://www.climatecongress.info/wiki/BotResource:usa_ca_upper_votes
#http://www.climatecongress.info/wiki/BotResource:usa_ca_votes
#leg_list = "usa_ca_upper_votes"

#http://www.climatecongress.info/wiki/BotResource:usa_ca_lower_votes
#leg_list = "usa_ca_lower_votes"

def get_leg_item(leg_list): ### legislationtext = get_leg_item(leg_list) ###Returns a list of legislation
    legislationpage = "BotResource:"+leg_list ##This block fetches the legislation of interest
    print ("Queried MediaWiki for "+ legislationpage)
    legislation = site.pages[legislationpage]
    legislation.exists #True or False
    legislationtext = legislation.text()
    legislationtext = legislationtext.split('\n')
    return legislationtext


leg_list = "usa_ca_votes" ### Results in http://www.climatepolitics.info/wiki/BotResource:usa_ca_votes
legislationtext = get_leg_item(leg_list) #print(legislationtext)



##This block fetches the page that will be updated
#http://www.climatecongress.info/wiki/Category:Candidates
#SpecifiedCategory = 'Candidates'

#state = 'ca'

#openstates.bill_detail( 'ca', '20152016', 'SB 32')
#openstates.bill_detail( 'ca', '20092010', 'AB 667')
#https://openstates.org/api/v1/bills/ca/20152016/SB%2032/
#https://openstates.org/api/v1/bills/ca/20152016/SB 32/
#openstates.bill_detail( state, session, bill)



#### Create a list of all the us_ca pages to be updated
list=[]
for a_page in site.Categories[Specified_A_Category]:
    list.append(a_page)
for a_page in site.Categories[Specified_B_Category]:
    list.append(a_page)

#### Update all those pages
for a_page in list:
    #print(a_page)
    articlepage = site.Pages[a_page]  #articlepage = site.Pages["Michael_Thompson"] #articlepage = site.Pages["Bill_Dodd_(USA_CA)"] #articlepage = site.Pages['Cathleen_Galgiani_(USA_CA)']

    #articlepage = site.Pages['Bill_Dodd_(USA_CA)']
    profiletext = articlepage.text()
    print("Updated Q2 auto-summary of: " + str(articlepage.name.encode('utf-8'))[2:-1])
    #return (profiletext, articlepage)
    #    print ("MW Queried for " + a_page + ", page exists?")
    #    page.exists #True or False


    '''
    def get_ca_leg_committees(legislationtext): ##get_ca_leg_committees ### Results in dict_ca_leg_com
        for line in legislationtext:
            data_legis = line.split(',')
            state = data_legis[0]
            session = data_legis[1]
            bill = data_legis[2]
            vote = openstates.bill_detail( state, session, bill)
            ## List committees that had actions on the bill
            list_committee = []
            for b in vote['actions']:
                for c in b['related_entities']:
                    if c['id'] is not None:
                        #print (c['id']) #get committee id#
                        list_committee.append(c['id'])
                    #https://openstates.org/api/v1/legislators/?state=ca&committee=CAC000751
                    #https://openstates.org/ca/committees/CAC000751/
                    #openstates.committee_detail('CAC000751')
        list_committee = list(set(list_committee))
        #list_committee = [x for x in list_committee if x is not None]
        print(list_committee)
        #heard_coms = []
        dict_ca_leg_comm = "[(" #{ 'a': 1, 'b': 2 }
        for a_comm in list_committee:
            if a_comm.startswith( 'CAC' ):
                print (a_comm)
                y = (openstates.committee_detail(str(a_comm)))
                a = str(y['chamber'] + " " +  y['committee']).replace('upper ', 'Senate ').replace('lower ', 'Assembly ')
                a.replace("'", "").replace("[", "").replace("]", "")
                print (a)
                dict_ca_leg_comm += "'" + str(a_comm) + "'" + ": " + "'"+ str(a)+ "',"
                #heard_coms = str(heard_coms).replace("'", "").replace("[", "").replace("]", "")
            #q2_abill_insert += str("\n\n Committees that had actions on this bill: " + str(heard_coms) )
            #heard_coms = []
        dict_ca_leg_comm = (dict_ca_leg_comm[:-2])
        dict_ca_leg_comm += ")]"
        print (dict_ca_leg_comm)
        dict_ca_leg_comm = dict(dict_ca_leg_comm[0])
        return (dict_ca_leg_comm)

    dict_ca_leg_comms =""
    dict_ca_leg_comms = get_ca_leg_committees(legislationtext)
    '''


    def get_q2_text(profiletext): ##get_q2_text ### Results in q2
        if "'''Automatically Generated Legislative Actions'''\n" in profiletext:
            q2start = (profiletext.index("'''Automatically Generated Legislative Actions'''\n"))
            tailtext = profiletext[q2start:]
            #print(str(tailtext).encode('utf-8'))
            q2end = (q2start+tailtext.index("}}"))
            q2 = profiletext[q2start:q2end]
            #print ("auto found")
            if "\n|" in tailtext:
                #print ("newtail")
                q2end = (q2start+tailtext.index("\n|"))+1
                q2 = profiletext[q2start:q2end]
                #print ("auto found2")
        elif "|Q2=" in profiletext:
            q2start = (profiletext.index("|Q2="))+4
            tailtext = profiletext[q2start:]
            q2end = (q2start + tailtext.index("}}"))
            #print ("q2 found")
            if "\n|" in tailtext:
                #print ("q2 found2")
                q2end = (q2start + tailtext.index("\n|"))+1
            q2 = profiletext[q2start:q2end]
            #print (q2)

            q2start = q2end
            q2 += "\n\n'''Automatically Generated Legislative Actions'''\n"
        else:
            #print("else found")
            q2end = (profiletext.index("}}"))
            q2start = (profiletext.index("}}"))
            q2 = profiletext[q2start:q2end]
            q2 += "\n\n'''Automatically Generated Legislative Actions'''\n"
        return (q2start, q2end, q2)

    q2result = get_q2_text(profiletext)
    q2start = q2result[0]
    q2end = q2result[1]
    q2 = q2result[2]

    #print ("q2")
    #print(str(profiletext[q2start:q2end]).encode('utf-8'))
    #print("tail end")
    #print(profiletext[q2end:])




    def get_profile_vars (profiletext):
        bioguide_id = "None"
        gender = "None"
        caleg_id = "None"
        firstname = "None"
        if "Bioguide_id=" in profiletext:
            bioidstart = (profiletext.index("Bioguide_id="))+12
            bioidend = bioidstart+7
            bioguide_id = profiletext[bioidstart:bioidend] #print(bioguide_id) #Bioguide_id noted to be 7 characters long, update script if proven otherwise
        if "Gender=" in profiletext:
            genderstart = (profiletext.index("Gender="))+7
            genderend = genderstart+1
            gender = profiletext[genderstart:genderend]  #print(gender) #Options should be limited to F(female) M(male) E(Enby/nonbinary) O(other)
        if "Leg_id=" in profiletext:
            calegidstart = (profiletext.index("Leg_id="))+7
            calegidend = calegidstart+9
            caleg_id = profiletext[calegidstart:calegidend] #caleg_id = "CAL000403" #Dodd test #print(caleg_id)
        firstnamestart = (profiletext.index("Firstname="))+10
        chunk = profiletext[firstnamestart:].index("\n")
        firstname = profiletext[firstnamestart:firstnamestart+chunk]    #print(firstname)
        return (bioguide_id, gender, caleg_id, firstname)

    profileresult = get_profile_vars (profiletext)
    bioguide_id = profileresult[0]
    gender = profileresult[1]
    caleg_id = profileresult[2]
    firstname = profileresult[3]
    #caleg_result = ca_leg_text(legislationtext, caleg_id, firstname) #### result is q2_abill_insert

    def ca_leg_text(legislationtext, caleg_id, firstname):
        q2_abill_insert = ""

        for line in legislationtext:
            data_legis = line.split(',')
            state = data_legis[0]
            session = data_legis[1]
            bill = data_legis[2]
           # print (state, session, bill)
            vote = openstates.bill_detail( state, session, bill)

            ## Get Legislation Role Value on Bill
            legislation_role = 0
            role = ""
            for cs in vote['sponsors']:
                #print("Role TEST")
                if str(cs).find(caleg_id) != -1:
                    if cs['type'] != 'other':
                        legislation_role = legislation_role+1
                        role = (cs['type'])
                        if role == 'cosponsor':
                            role = 'a cosponsor'
                        if role == 'sponsor':
                            role = 'a sponsor'
                        if role == 'primary':
                            role = 'an author'
                        #print ("role" + str(bill))

            ## Get Legislation Action Value on Bill
            legislation_action = 0
            #print("Leg TEST")
            for cs in vote['votes']:
                #if str(cs).find(caleg_id) != -1:
                    #print (str(cs['type']))
                    #legislation_action = legislation_action+1
                if str(cs['yes_votes']).find(caleg_id) != -1:
                    legislation_action = legislation_action+1

                if str(cs['no_votes']).find(caleg_id) != -1:
                    legislation_action = legislation_action+1
                    #    legislation_action = legislation_action-1
                    #print ("Leg action " + str(bill))

            if legislation_action + legislation_role > 0:

                # The legislators votes
                #print (str((vote["bill_id"]).encode('utf-8')))
                #print (str((vote['summary']).encode('utf-8')))

                vote_url = ""
                vote_session = ""
                ##vote_url = vote['versions']
                ##vote_url = vote_url[0]
                ##vote_url = vote_url['url']
                ##vote_url = vote_url.replace("billNavClient", "billVotesClient")
                #CA LEG VOTE URL ABOVE INTERNAL BELOW
                #Example
                #vote_url = [[2015-2016 SB32 (USA CA)|SB 380]]
                vote_session = vote['session']
                vote_session = str(vote_session[:4])+"-"+str(vote_session[4:])
                bill_link = vote_session +" "+ bill.replace(" ","")+" "+"(USA CA)"
                vote_url = bill_link+"|"+bill

                #print ("action/role: " + str(legislation_action) +"/" + str(legislation_role) + " " + str(bill))
                ## Bill intro line
                q2_abill_insert += ("\n\n'''" + "[["+str(vote_url)+ "]]" + " " + vote['title'] + "'''" ) # '''[http://ClimateCongress.us ClimateCongress.us]''' #print ("\n\n" + bill + ": " + vote['title'])
                #With description q2_abill_insert += ("\n\n'''" + bill + " " + vote['title'] + "'''"+ '\n\n' + "''" + str(vote['+impact_clause'])+ "''" ) # '''[http://ClimateCongress.us ClimateCongress.us]''' #print ("\n\n" + bill + ": " + vote['title'])
                ## Final Actions (Passed/Signed)
                if legislation_role > 0:
                    q2_abill_insert += (str("\n\n"+firstname + " was " + role + " of "+ bill + "."))
                    #print("Role added")
                for y in vote['actions']:
                    if (y['type']) == ['amendment:passed']:
                        q2_abill_insert += ("\n\nFinal legislative action " + (str(datetime.datetime.strptime(str(y['date']), '%Y-%m-%d %H:%M:%S').date())) + " passed yeas " + str(y['+yes_votes']).replace("'", "").replace("[", "").replace("]", "") + ", nays " + str(y['+no_votes']).replace("'", "").replace("[", "").replace("]", "") +". "  )
                        #print("yes")
                    ##if (y['type']) == ['governor:signed']:
                    ##    q2_abill_insert += str("\n\n" + (str(datetime.datetime.strptime(str(y['date']), '%Y-%m-%d %H:%M:%S').date())) + " Governor signed"  )
                    ##    #print("yes")



                #http://leginfo.legislature.ca.gov/faces/billVotesClient.xhtml?bill_id=201520160SB32%20billVotesClient%20billNavClient
                for x in vote['votes']:
                    if str(x).find(caleg_id) != -1:   #print(str(x).find(caleg_id))
                        ##try:
                        ##    committee = str(x['committee'])
                        ##    pass
                        ##except KeyError:
                        ##    committee = "Floor Action"
                        ##    pass
                        ##q2_abill_insert += ("\n:*On " + str(str(datetime.datetime.strptime(str(x['date']), '%Y-%m-%d %H:%M:%S').date())) + " Committee: " + committee + " yeas " + str(x['yes_count']) + ", nays " + str(x['no_count']) + ". Passed: " + str(x['passed']))
                        #q2_abill_insert += ("\n:*On " + str(str(datetime.datetime.strptime(str(x['date']), '%Y-%m-%d %H:%M:%S').date())) + " yeas " + str(x['yes_count']) + ", nays " + str(x['no_count']) + ". Passed: " + str(x['passed']))
                        #print (str(x).encode('utf-8'))
                        if str(x['yes_votes']).find(caleg_id) > 1:
                            q2_abill_insert += ("\n:*" + firstname + " voted yea (in favor of " + str(x['motion'])+ ")." )
                            #q2_abill_insert += ("\n:**On " + str(str(datetime.datetime.strptime(str(x['date']), '%Y-%m-%d %H:%M:%S').date())) + " " + firstname + " voted yea, in favor of the action: " + str(x['motion']))
                        if str(x['no_votes']).find(caleg_id) > 1:
                            q2_abill_insert += ("\n:*" + firstname + " voted nay (against " + str(x['motion']) + ")." )

        if q2_abill_insert.endswith( '<!--EndQ2-->\n|' ):
            return (q2_abill_insert)
        else:
            q2_abill_insert += "\n<!--EndQ2-->\n|\n"
            return (q2_abill_insert)

            #Voting other
            #if str(x['other_votes']).find(caleg_id) > 1:
            #    q2_abill_insert += ("\n:**On " + str(str(datetime.datetime.strptime(str(x['date']), '%Y-%m-%d %H:%M:%S').date())) + " " + firstname + " voted other in regards to the action: " + str(x['motion']))
            #q2_abill_insert += (str(bill) + "/n/n action dates are: " +  str(vote['action_dates']) + "/n/n URL is: " + str(vote['versions']['url']))


    caleg_result = ca_leg_text(legislationtext, caleg_id, firstname) #### result is q2_abill_insert

    caleg_text = caleg_result
    start_section = profiletext[:q2start]
    end_section = profiletext[q2end:]

    def create_q2_insert(profiletext,caleg_text):
        q2_insert = ""
        q2_insert = "\n\n'''Automatically Generated Legislative Actions'''\n"
        if "|Q2=" not in profiletext:
            q2_insert = "\n\n|Q2=  \n\n'''Automatically Generated Legislative Actions'''\n"
        q2_insert += str(caleg_text)
        return (q2_insert)

    q2_insert = ""
    #print ("next")
    #print(end_section)
    q2_insert = create_q2_insert(profiletext,caleg_text)
    newtext = start_section+q2_insert+end_section
    articlepage.save(newtext, 'Votes Updated (vote bot v02)')
#    print("UPDATED!")





















    '''
    for y in x['actions']:
            if (y['type']) == ['amendment:passed']:
                print (y)

    vote = openstates.bill_detail( state, session, bill)
    openstates.committee_detail('CAC000751')

    https://openstates.org/api/v1/committees/CAC000751/
    #https://openstates.org/api/v1/legislators/?state=ca&committee=CAC000774
    #https://openstates.org/ca/committees/CAC000774/

    https://openstates.org/api/v1/committees/CAC000751/

            print ( y['date'] + " " +  y['action'] )

    ("Committee: " + x["committee"] + "\n\n Nay/Yea count: " + x[no_count] + "/" + x[yes_count] + " Passed: " + x[passed])
    "motion": "Do pass as amended and be re-referred to the Committee on [Appropriations]",
    "chamber": "lower",
    '''





    #a_page.save(newtext, 'Votes Updated (vote bot v01)')
    #print("Updated Q2 auto-summary of: " + str(articlepage.name.encode('utf-8')))



    #profiletext = articlepage.text()
    #['Cathleen_Galgiani_(USA_CA)'].save(newtext, 'Votes Updated (vote bot v01)')
    #print("Updated Q2 auto-summary of: " + str(articlepage.name.encode('utf-8')))


    '''
    def get_a_page(site, SpecifiedCategory): ##def get_a_page ### Results in text (maybe only one and not loop)
        for a_page in site.Categories[SpecifiedCategory]:
            listpage = site.Pages[a_page]  #listpage = site.Pages["Michael_Thompson"] #listpage = site.Pages["Bill_Dodd_(USA_CA)"] #listpage = site.Pages['Cathleen_Galgiani_(USA_CA)']
            profiletext = listpage.text()
    '''



    '''
    ###To Create a new page listing all the candidates category pages.
    import mwclient
    site = mwclient.Site(('https', 'en.wikipedia.org'))
    site.login('username', 'password')
    listpage = site.Pages['User:Antoine/categoryCandidatespages']
    text = listpage.text()
    for page in site.Categories['Candidate']:
        text += "* [[:" + page.name + "]]\n"
    listpage.save(text, summary='Creating list from [[Category:Candidate]]')


    print (firstname + " voted " + vote['bill_id'] + " " + vote['title']+"\n"+"Official site: " + "https://leginfo.legislature.ca.gov/faces/billNavClient.xhtml?bill_id="+session+"0"+bill.replace(" ", "") + "\n" + "Alternative Title(s): " + str(vote['alternate_titles'])+"\n" )
    #"Summary: " + str(vote['summary'].encode("utf8")))



    upper_var['title']
    lower_var['title']

    upper_var['motion']
    lower_var['motion']


    lower_var = vote['votes'][0]
    for x in vote['votes']:
        if x['chamber'] == 'lower':

    for x in vote['votes']:
        if x['chamber'] == 'lower':
            print("Assembly motion: " + x['motion'])
            if str(x).find(caleg_id):
                if str(x['yes_votes']).find(caleg_id):
                    print (firstname + " voted yes in favor of the motion "+ x['motion'])
                    pass
                elif str(x['no_votes']).find(caleg_id):
                    print (firstname + " voted no in against the motion "+ x['motion'])
                    pass
                elif str(x['other_votes']).find(caleg_id):
                    print (firstname + " voted other in regards to the motion "+ x['motion'])
                    pass

    print (bill + ": " + vote['title'])
    #print (bill + ": " + vote['title'] + vote['summary'])

    for x in vote['votes']:
        if x['chamber'] == 'lower':
            if str(x).find(caleg_id):
                if str(x['yes_votes']).find(caleg_id):
                    print (str(datetime.datetime.strptime(str(x['date']), '%Y-%m-%d %H:%M:%S').date()) + " In relation to " +bill+ ", " + firstname + " voted yea, in favor of the action: "+ x['motion'])
                    pass
                elif str(x['no_votes']).find(caleg_id):
                    print (str(datetime.datetime.strptime(str(x['date']), '%Y-%m-%d %H:%M:%S').date()) + " In relation to " +bill+ ", " + firstname + " voted nay, against the action: "+ x['motion'])
                    pass
                elif str(x['other_votes']).find(caleg_id):
                    print (str(datetime.datetime.strptime(str(x['date']), '%Y-%m-%d %H:%M:%S').date()) + " In relation to " +bill+ ", " + firstname + " voted other in regards to the action: "+ x['motion'])
                    pass
                #print("Senate motion: " + x['motion'])





    q2_abill_insert = (bill + ": " + vote['title'])
    q2insert += '\n'
    for x in vote['votes']:
      if str(x).find(caleg_id):
          if str(x).find(caleg_id) > 1:
              q2_abill_insert += (str(datetime.datetime.strptime(str(x['date']), '%Y-%m-%d %H:%M:%S').date()) + " In relation to " +bill+ ", " + firstname + " voted yea, in favor of the action: "+ x['motion'])
              q2_abill_insert += '\n'
              pass
          if str(x['no_votes']).find(caleg_id) > 1:
              q2_abill_insert += (str(datetime.datetime.strptime(str(x['date']), '%Y-%m-%d %H:%M:%S').date()) + " In relation to " +bill+ ", " + firstname + " voted nay, against the action: "+ x['motion'])
              q2_abill_insert += '\n'
              pass
          if str(x['other_votes']).find(caleg_id) > 1:
              q2_abill_insert += (str(datetime.datetime.strptime(str(x['date']), '%Y-%m-%d %H:%M:%S').date()) + " In relation to " +bill+ ", " + firstname + " voted other in regards to the action: "+ x['motion'])
              q2_abill_insert += '\n'
              pass



          #print("Senate motion: " + x['motion'])

    if str(x['yes_votes']).find(caleg_id) == 2:


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
