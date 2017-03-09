import mwclient
from mwclient import Site
import re
import sunlight
from sunlight import openstates
import os


upper = openstates.legislators(state='ca',chamber='upper')
lower = openstates.legislators(state='ca',chamber='lower')



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

save_note = "Bot creating US CA profiles"
default = "" #Create a result for dictionary response when key does not occure
count = 0

for x in upper:
    new_page = a_page = insert = fn = a = b = c = d = e = f = g = h = i = j = k = l = m = n = o = p = q = r = ""
    a = '{{US CA Upper' +'\n'
    fn = str(x.get("first_name", default)) #BC first_name includes unwanted middle initials
    fn = str(re.sub(' .*', '', fn))  #BC first_name includes unwanted middle initials
    b = '|Firstname=' + fn +'\n'
    c = '|Lastname=' + str(x.get("last_name", default)) +'\n'
    d = '|Middlename=' + str(x.get("Middle_name", default)) +'\n'
    e = '|Nickname=' + str(x.get("Nickname", default)) +'\n'
    f = '|Gender=' + str(x.get("NOVALUE", default)) +'\n'
    g = '|Office=CA State Senator' +'\n'
    h = '|State=California' +'\n'
    i = '|Wing=Upper' +'\n'
    j = '|Level=US_State' +'\n'
    k = '|District=' + str(x.get("district", default)) +'\n'
    l = '|Party=' + str(x.get("party", default)) +'\n'
    m = '|OfficialGovSite=' + str(x.get("url", default)) +'\n'
    n = '|AdditionalSite=' + str(x.get("NOVALUE", default)) +'\n'
    o = '|Photo=' + str(x.get("photo_url", default)) +'\n'
    p = '|Votesmart_id=' + str(x.get("votesmart_id", default)) +'\n'
    q = '|Leg_id=' + str(x.get("leg_id", default)) +'\n'
    r = '}}'
    insert = (a + b + c + d + e + f + g + h + i + j + k + l + m + n + o + p + q + r)
    new_page = str(fn + "_" + str(x.get("last_name", default)) + " (USA_CA)")
    a_page = site.Pages[new_page]
    if a_page.exists == False:
        a_page.save(insert, save_note)
        count = count + 1
        print (count)
    else:
        print("Page already exists, will not overwrite")

for x in lower:
    new_page = a_page = insert = fn = a = b = c = d = e = f = g = h = i = j = k = l = m = n = o = p = q = r = ""
    a = '{{US CA Lower' +'\n'
    fn = str(x.get("first_name", default)) #BC first_name includes unwanted middle initials
    fn = str(re.sub(' .*', '', fn))  #BC first_name includes unwanted middle initials
    b = '|Firstname=' + fn +'\n'
    c = '|Lastname=' + str(x.get("last_name", default)) +'\n'
    d = '|Middlename=' + str(x.get("Middle_name", default)) +'\n'
    e = '|Nickname=' + str(x.get("Nickname", default)) +'\n'
    f = '|Gender=' + str(x.get("NOVALUE", default)) +'\n'
    g = '|Office=CA State Assemblymember' +'\n'
    h = '|State=California' +'\n'
    i = '|Wing=Lower' +'\n'
    j = '|Level=US_State' +'\n'
    k = '|District=' + str(x.get("district", default)) +'\n'
    l = '|Party=' + str(x.get("party", default)) +'\n'
    m = '|OfficialGovSite=' + str(x.get("url", default)) +'\n'
    n = '|AdditionalSite=' + str(x.get("NOVALUE", default)) +'\n'
    o = '|Photo=' + str(x.get("photo_url", default)) +'\n'
    p = '|Votesmart_id=' + str(x.get("votesmart_id", default)) +'\n'
    q = '|Leg_id=' + str(x.get("leg_id", default)) +'\n'
    r = '}}'
    insert = (a + b + c + d + e + f + g + h + i + j + k + l + m + n + o + p + q + r)
    new_page = str(fn + "_" + str(x.get("last_name", default)) + " (USA_CA)")
    a_page = site.Pages[new_page]
    if a_page.exists == False:
        a_page.save(insert, save_note)
        count = count + 1
        print (count)
    else:
        print("Page already exists, will not overwrite")
