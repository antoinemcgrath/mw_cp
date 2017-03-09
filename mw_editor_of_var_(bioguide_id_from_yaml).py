#!/usr/bin/env python
#--Python3 script
#python3 /Users/macbook/ccc/MW_var_addition_script.py

import yaml
import pandas as pd
import mwclient
from mwclient import Site #import mwclient
import sys
import mwclient
import json
import re
from mwclient import Site #import mwclient
import csv
import os

#import subprocess #needed

##This block defines variables
SpecifiedCategory = 'Candidates'
profiles_checked = 0
updated = 0

##This block sets MediaWiki (MW) access



##This block fetches the legislation of interest
legislationpage = "BotResource:US_Congressional_Legislation"
print ("Queried MediaWiki for "+ legislationpage)
legislation = site.pages[legislationpage]
legislation.exists #True or False
legislationtext = legislation.text()
#print(legislationtext)


##This block fetches the page from category to be updated
'''
#testing
listpage = site.Pages['Danny_Davis']
text = listpage.text()
search_for = "|Bioguide_id="
start = 'Firstname='
end = '\n'
first = re.search('%s(.*)%s' % (start, end), text).group(1)
start = 'Lastname='
end = '\n'
last = re.search('%s(.*)%s' % (start, end), text).group(1)
start = 'District='
end = '\n'
district = re.search('%s(.*)%s' % (start, end), text).group(1)
district = int(district)
f  = open('/Users/macbook/ccc/@unitedstates/congress-legislators-master/legislators-current.yaml', 'r', encoding='utf-8')
df = pd.io.json.json_normalize(yaml.load(f))
f.close()
##Check if YAML contains matching lastname
#p_lasts = df['name.last'].str.contains(last, na=False) #Long list of True and False
p_lasts = df[df['name.last'].str.contains(last, na=False)] #Full list of item
p_lasts = df[df['name.last'].str.contains(last, na=False)][['name.first', 'name.last', 'bio.gender', 'id.bioguide']]
##Check if matches have matching first names
p_firsts= p_lasts['name.first'].str.contains(first, na=False)
p_firsts= df[p_lasts['name.first'].str.contains(first, na=False)['name.first', 'name.last', 'bio.gender', 'id.bioguide']]
p_firsts= p_lasts['name.first'].str.contains(first, na=False)[['p_lasts.name.first]]

p_lasts = df[df['name.last'].str.contains(last, na=False)][['name.first', 'name.last', 'bio.gender', 'id.bioguide']]
p_firsts = p_lasts[p_lasts['name.first'].str.contains(first)]
bi = str(list(p_firsts['id.bioguide']))[3:-2]

p_firsts.object[2]

groupDF.loc[(groupDF['Rank']==2),'Name'].item()
p_firsts.loc[(p_firsts['id.bioguide']==2),'id.bioguide'].item()



p_firsts
data = pd.get_dummies(data, prefix=list_)
p_firsts = pd.get_dummies(p_firsts)

data = p_firsts.(id.bioguide)(data, prefix=list_)
return data



p_firsts= p_lasts['name.first'].str.contains(first, na=False)[['first', 'last', 'gender', 'bioguide']]
#p_district= p_lasts['terms.district'].contains(district, na=False)
'''


for a_page in site.Categories[SpecifiedCategory]:
    listpage = site.Pages[a_page]  #print (listpage)
#    print ("Queried MediaWiki for " + a_page + ", page exists?")
#    page.exists #True or False
    profiles_checked += 1
    text = listpage.text()

##This block determines if the page has a Bioguide_id field,
    search_for = "|Bioguide_id="
    if text.find(search_for) == -1:
        #print ("No " + search_for + " here! Profiles checked = " + str(profiles_checked))
        start = 'Firstname='
        end = '\n'
        first = re.search('%s(.*)%s' % (start, end), text).group(1)
        start = 'Lastname='
        end = '\n'
        last = re.search('%s(.*)%s' % (start, end), text).group(1)
        end_of_lastname = re.search('%s(.*)%s' % (start, end), text).end()
        #print (end_of_lastname)
        '''start = 'District='
        end = '\n'
        district = re.search('%s(.*)%s' % (start, end), text).group(1)
        district = int(district)
        #print("Processing the page of: " + first + " " + last)
        '''



        ##This block opens a YAML from @unitedstates .io profiling members of the current congress
        f  = open('/Users/macbook/ccc/@unitedstates/congress-legislators-master/legislators-current.yaml', 'r', encoding='utf-8')
        df = pd.io.json.json_normalize(yaml.load(f))
        f.close()

        p_lasts = df[df['name.last'].str.contains(last, na=False)][['name.first', 'name.last', 'bio.gender', 'id.bioguide']]
        p_firsts = p_lasts[p_lasts['name.first'].str.contains(first)]
        bi = str(list(p_firsts['id.bioguide']))[2:-2]
        gen = str(list(p_firsts['bio.gender']))[2:-2]
        if bi:
            #print (bi)
            #print (gen)
            new_vars = '|Bioguide_id='+bi+'\n' + '|Gender='+gen+'\n'
            new_vars += text[end_of_lastname:]
            newtext = text[0:end_of_lastname] + new_vars
            a_page.save(newtext, 'Bioguide_id and Gender added (bio_gen updator bot v01)')
            updated += updated + 1
            #print("Updated " + str(updated))
            print(str(a_page.name.encode('utf-8')) + "," + bi + "," + gen)
        else:
            #print ("bi is empty")
            pass


        ##Check if YAML contains matching lastname
        #p_lasts = df[df['name.last'].str.contains(last, na=False)]
        ##Check if matches have matching first names
        #p_firsts= p_lasts['name.first'].str.contains(first, na=False)
        #p_district= p_firsts['terms.district'].str.contains(district, na=False)

        #pan = df[df[['name.last'].str.contains(last, na=False),['name.first'].str.contains(first, na=False)]]
        #pandas_last = df['name.last'].str.contains(last)
        #pandas_first =df['name.first'].str.contains(first)




##Continues: This block determines if the page has a Bioguide_id field,
    else:
        #print ("PASS BIOGUIDE ID GENERATION Found " + search_for + " on the page of: " + str(listpage) + " Profiles checked = " + str(profiles_checked))
        pass

#    page = site.pages[thepage]
#    text = page.text()
#{Candidate\n|Firstname=Michael\n|Lastname=Thompson\n|State=California\n|District=5\n|Office=House\n|Party=Democratic\n|Bioguide_id=T000460\n|Gender=Male\n|Q1=\n|Q2=\n\n

#listpage = site.Pages['User:Antoine/categoryCandidatespages']
#text = listpage.text()
#for page in site.Categories['Candidate']:
#    text += "* [[:" + page.name + "]]\n"

#page = site.Pages[pagename]
#page.delete(reason='Spam Page', watch=True)
#print ("Deleted")
'''
df.get_value(0, 'name.official_full', takeable=False)
#df['name.first'].str.contains('Liz')
df['name.first'].str.contains(first)
df['name.nickname'].str.contains(first, na=False)
df[df['name.first'].str.contains(first, na=False)][['name.first', 'name.last', 'bio.gender']][0:5]
print df[df.Resource.str.contains('pdf',na=False)][['IP', 'Time', 'Resource']][0:5]

print(df.head(0))

df['name.nickname'].str.contains(first)

print(df.head(0))

'''

'''
print(df.head())
df ['name.first'].value_counts()[:5]


import io
from PIL import Image
import matplotlib.pyplot as plt

plt.figure()
plt.plot(df ['name.first'].value_counts()[:5])
plt.title("test")

buf = io.BytesIO()
plt.savefig(buf, format='png')
buf.seek(0)
im = Image.open(buf)
im.show()
buf.close()


import pandas as pd
import yaml
with open('data.yaml', 'r') as f:
df = pd.io.json.json_normalize(yaml.load(f))
df ['name.first'].value_counts()[:5]
print(df.head())



try:
 for key, value in yaml.load(open('/Users/macbook/ccc/@unitedstates/congress-legislators-master/legislators-current.yaml'))[key]['bio'].iteritems():
   print key, value
except yaml.YAMLError as out:
  print(out)
'''
