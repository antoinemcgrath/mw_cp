#MediaWiki
#cd /Users/macbook/ccc/govtrack_us/
# python3 /Users/macbook/Documents/GITS/mediawiki/mw_usa_congress_updator.py
#python3

#http://mwclient.readthedocs.io/en/latest/user/index.html

import mwclient
import json
import re
import csv
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




leg_list = "usa_congress_votes"
legislationpage = "BotResource:"+leg_list

##This block fetches the legislation of interest
print ("Queried MediaWiki for "+ legislationpage)
legislation = site.pages[legislationpage]
legislation.exists #True or False
legislationtext = legislation.text()
#print(legislationtext)

##This block fetches the page that will be updated
SpecifiedCategory = 'Candidates'
for a_page in site.Categories[SpecifiedCategory]:
    listpage = site.Pages[a_page]  #print (listpage)
#    print ("Queried MediaWiki for " + a_page + ", page exists?")
#    page.exists #True or False
    text = listpage.text()
    if "|Q2=" in text:
        #print ("Q2 already exists in " + str(a_page.name.encode('utf-8')))
        #q2end = (text.index("|Q3="))-1 #1589
        #q2start = (text.index("|Q2="))+4 #1589
        #q2 = text[q2start:q2end]
        #q2autostart = q2end
        pass
    else:
        if "Bioguide_id=" in text and "Gender=" in text:
            textstart = 0
            textend = len(text)
            ##Set the necessary legislative generator variables
            bioidstart = (text.index("Bioguide_id="))+12
            bioidend = bioidstart+7
            bioguide_id = text[bioidstart:bioidend]
            #print(bioguide_id) #Bioguide_id noted to be 7 characters long, update script if proven otherwise
            genderstart = (text.index("Gender="))+7
            genderend = genderstart+1
            gender = text[genderstart:genderend]
            #print(gender) #Options should be limited to F(female) M(male) E(Enby/nonbinary) O(other)

            q2end = (text.index("}}"))-1
            q2start = q2end
            q2 = text[q2start:q2end]


            q2autostart = q2end
            #q2autostart = text.index("\n\n'''Automatically Generated Congressional Votes'''") #Will remain the same if it does not exist

            astring = "\n\n'''Automatically Generated Congressional Votes'''"

            #for text in text:
            if astring in text:
                q2autostart = text.index("\n\n'''Automatically Generated Congressional Votes'''") #Will remain the same if it does not exist
            else:
                q2autostart = q2end

            q2autoend = q2end
            #global q2autoinsert
            q2autoinsert = ("\n\n'''Automatically Generated Congressional Votes'''")


            start = text[textstart:q2autostart]
            end = text[q2autoend:textend]
            #insert = text[(text.index("Automatically Generated Congressional Votes"))+49:q2end]
            #q2start = (text.index("|Q2="))+4 #1573
            #q2auto = text[q2start:q2end]
            #print(text[q2start:q2end])   #print(text[1577:1592])








            #Get the vote result from the json of a particlar id and see if it is nested as
            def get_vote_cast_from_id(id):
                #global json_votefile
                #name = "None"
            ##    for name, nested_values in json_data['votes'].items():
                for name, nested_values in json_data['votes'].items():

                    if any(nested_value['id'] == id for nested_value in nested_values):
                        global name
                        #print(name)
                        return name
                else:
                    name = "None"
                    #print ("none")
                    return None


            def generate_q2_autoinsert_texts(bioguide_id, gender, q2autoinsert):
                ##for bioguide_id in bioguide_id:    ##line = list
                id = bioguide_id ##id = list[10]
            #    gender = gender ##gender = list[8] ##lastname = list[2]     ##first_name = list[0]     #print Last_Name
                if id == "":
                    #print ("Empty BIOID Field")
                    pass
                elif gender == "": #print "Empty Field: gender"
                    pass
                elif gender == " ": #print "Empty Field: gender"
                    pass
                else: ##print lastname + " " + first_name + " " + id
                    legiss=legislationtext.split('\n')
                    for line in legiss:

                        data_legis = line.split(',')
                        #print (data_legis)
            #        print (data_legis)
            #        for line in data_legis:
            #            print(line)
                        # Vote look up will occur in various data.json files
                        # session, year, wing are required to navigate to the correct data.json file (json_votefile)
                        # For example a valid filepath value (json_votefile) is: /Users/macbook/ccc/govtrack_us/112/votes/2011/S54/data.json
                        #print (line)
                        session = data_legis[0]
                        #print(session)
                        year = data_legis[1]
                        #print(year)
                        wing = data_legis[2]
                        #print(wing)
                        vote = data_legis[3]
                        #print(vote)

                        if session == "":               #print "Empty Field: Congressional Session"
                            pass
                        elif year == "":                #print "Empty Field: Year"
                            pass
                        elif wing == "":                #print "Empty Field: Wing"
                            pass
                        elif vote == "":                #print "Empty Field: Vote"
                            pass
                        else:
                            json_votefile = "/Users/macbook/ccc/govtrack_us/" + str(session) + "/votes/" + str(year) + "/" + str(wing) + str(vote) + "/data.json"
                            json_votefile = str(json_votefile) #print id +" "+ json_votefile
                            json_vote = open(json_votefile).read()
                            global json_data
                            json_data = json.loads(json_vote)
                            get_vote_cast_from_id(id)
                            #print json_vote
                            #values_summary = str(session) + "::" + str(year) + "::" + str(wing) + "::" + str(vote) + "::" + gender
                            #print values_summary
                            if name == "":                      #    print "Empty Field: name"
                                pass
                            elif name == "None":                #    print "Empty Field: name is none"
                                pass
                            elif name == "Not Voting":          #    print "Not Voting"
                                pass
                            else:                               #print json_votefile + " " + id + " " + name + " " + gender + " " + first_name
                                values_summary = str(session) + "::" + str(year) + "::" + str(wing) + "::" + str(vote) + "::" + name
                                #print (values_summary)

                                #gender F/M/E/O F(female) M(male) E(Enby/nonbinary) O(other)
                                # Set Mx/mx
                                # More info: https://en.wikipedia.org/wiki/Mx_(title)
                                # Further: http://nonbinary.org/wiki/Gender_neutral_language_in_English
                                if gender == "F":
                                    Mx = "She"
                                    mx = "she"
                                if gender == "M":
                                    Mx = "He"
                                    mx = "he"
                                if gender == "O":
                                    Mx = "They"
                                    mx = "they"
                                if gender == "E":
                                    Mx = "They"
                                    mx = "they"
                                #print (Mx)
                                #print (mx)    #print values_summary

                                if values_summary == "111::2009::H::477::Aye":
                                    q2autoinsert +="\n\nIn 2009, as a member of the US House of Representatives, " + mx + " voted for the American Clean Energy and Security Act HR 2454 (Waxman-Markey). https://www.congress.gov/bill/111th-congress/house-bill/2454 "
                                    #print (q2autoinsert)
                                    pass
                                if values_summary == "111::2009::H::477::No":
                                    q2autoinsert +="\n\nIn 2009, as a member of the US House of Representatives, " + mx + " voted against the American Clean Energy and Security Act HR 2454 (Waxman-Markey). https://www.congress.gov/bill/111th-congress/house-bill/2454 "
                                    #print (q2autoinsert)
                                    pass
                                if values_summary == "112::2011::H::249::Nay":
                                    q2autoinsert +="\n\nIn 2011, "+ mx + " voted against limiting the EPA's ability to regulate greenhouse gas emissions. http://clerk.house.gov/evs/2011/roll249.xml "
                                    #print (q2autoinsert)
                                    pass
                                if values_summary == "112::2011::H::249::Yea":
                                    q2autoinsert +="\n\nIn 2011, "+ mx + " voted to limit the EPA's ability to regulate greenhouse gas emissions. http://clerk.house.gov/evs/2011/roll249.xml "
                                    #print (q2autoinsert)
                                    pass
                                if values_summary == "114::2015::H::384::Aye":
                                    q2autoinsert +="\n\nIn 2015, as a member of Congress, " + mx + " supported HR 2042, the Ratepayer Protection Act, which would have prevented implementation of the Clean Power Plan. http://clerk.house.gov/evs/2015/roll384.xml "
                                    #print (q2autoinsert)
                                    pass
                                if values_summary == "114::2015::H::384::No":
                                    q2autoinsert +="\n\nIn 2015, as a member of Congress " + mx + " voted against HR 2042, the Ratepayer Protection Act, which would have prevented implementation of the Clean Power Plan. http://clerk.house.gov/evs/2015/roll384.xml "
                                    #print (q2autoinsert)
                                    pass
                                if values_summary == "113::2013::H::445::Aye":
                                    q2autoinsert +="\n\nIn 2013, "+ mx + " voted to make it harder for Congress to put a price on carbon by voting for a point of order opposing a carbon tax or a fee on carbon emissions. http://clerk.house.gov/evs/2013/roll445.xml "
                                    #print (q2autoinsert)
                                    pass
                                if values_summary == "113::2013::H::445::No":
                                    q2autoinsert +="\n\nIn 2013, "+ mx + " voted against making it harder for Congress to put a price on carbon by voting against a point of order opposing a carbon tax or a fee on carbon emissions. http://clerk.house.gov/evs/2013/roll445.xml "
                                    #print (q2autoinsert)
                                    pass
                                if values_summary == "113::2014::H::103::Aye":
                                    q2autoinsert +="\n\nIn 2014, " + mx + " voted for a House amendment calling on Congress to recognize that man-made carbon pollution contributes to climate change and that climate change has a wide range of negative effects. http://clerk.house.gov/evs/2014/roll103.xml "
                                    #print (q2autoinsert)
                                    pass
                                if values_summary == "113::2014::H::103::No":
                                    q2autoinsert +="\n\nIn 2014, "+ mx + " voted against a House amendment calling on Congress to recognize that man-made carbon pollution contributes to climate change and that climate change has a wide range of negative effects. http://clerk.house.gov/evs/2014/roll103.xml "
                                    #print (q2autoinsert)
                                    pass
                    global q2autoinsertion
                    #print (q2autoinsert)
                    #print ("All looks good")
                    q2autoinsertion = q2autoinsert


            #get_vote_cast_from_id(id)
            generate_q2_autoinsert_texts(bioguide_id, gender, q2autoinsert)
            #print (q2autoinsertion)
            newtext = start+"\n\n|Q2="+q2autoinsertion+end
            #newtext = start+q2autoinsertion+end
            a_page.save(newtext, 'Votes Updated (vote bot v01)')
            print("Updated legislation summary of: " + str(a_page.name.encode('utf-8')))
            #print("Updated " + a_page.name + " with: " + q2autoinsertion)


        else:
            #print ("Bioguide or Gender do not exist in: " + str(a_page.name))
            pass


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
'''
