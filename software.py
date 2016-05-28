import csv
from csv import DictReader
import re
import pandas as pd
from bs4 import BeautifulSoup
import urllib.request as urllib2

# read the table 
yahoo = csv.reader(open('software.csv'))
company_ticket_list=[]
for row in yahoo:
    company_ticket = row[0]
    pattern = "\((.*)\.(.*)\)"
    match = re.compile(pattern).search(row[0])
    if not match:
        company_ticket_list.append(row)

# get all the info
company_list=[]
ticket_list=[]
#marketcap_list=[]
for i in range(2,len(company_ticket_list)):
    company_name = company_ticket_list[i][0].split(' (')[0]
    ticket_name = company_ticket_list[i][0].split(' (')[1].split(')')[0]
    #marketcap_amount = company_ticket_list[i][2]
    company_list.append(company_name)
    ticket_list.append(ticket_name)
    #marketcap_list.append(marketcap_amount)

# clean duplicated
company_combine = []
for i in range(len(company_list)):
    tmp = []
    tmp.append(company_list[i])
    tmp.append(ticket_list[i])
    #tmp.append(marketcap_list[i])
    company_combine.append(list(tmp))

seen = []
uniq = []
for i in company_combine:
    if i not in seen:
        uniq.append(i)
        seen.append(i)

uniq_company_list = []
uniq_ticket_list = []
for i in range(len(uniq)):
    company_list2 = uniq[i][0]
    uniq_company_list.append(company_list2)
    ticket_list2 = uniq[i][1]
    uniq_ticket_list.append(ticket_list2)

# get detail for every company
ticket_list = uniq_ticket_list
sector_list=[]
industry_list=[]
summary_list=[]
country_list = []
url_preifx = "http://finance.yahoo.com/q/pr?s="
acturalurl=[]
for i in list(range(len(ticket_list))):
    actural = url_preifx + ticket_list[i]
    acturalurl.append(actural)

for i in range(len(ticket_list)):
    req = urllib2.Request(acturalurl[i])
    response = urllib2.urlopen(req)
    html = response.read()
    soup = BeautifulSoup(html)
    try: 
        summary = soup.findAll('tr', { "valign" : "top"})[0].find('p').find(text=True)
    except:
        summary = ' '
    summary_list.append(summary)
    try: 
        sector = soup.find(text='Sector:').next.find(text=True)
    except:
        sector = ' '
    sector_list.append(sector)
    try: 
        industry = soup.find(text='Industry:').next.find(text=True)
    except:
        industry = ' '
    industry_list.append(industry)
    try:
        cou = soup.findAll('td', {"class" : "yfnc_modtitlew1"})[0].findAll(text = True)
        for i in range(len(cou)):
            if ' - ' in cou[i]:
                country = cou[i].split(' -')[0]
    except:
        country = ' '
    country_list.append(country)

    print(len(industry_list))

'''
# get country
acturalurl2=[]
for i in list(range(len(ticket_list))):
    actural2 = url_preifx + ticket_list[i] + "+Profile"
    acturalurl2.append(actural2)

#test
req = urllib2.Request("http://finance.yahoo.com/q/pr?s=WUBA+Profile")
response = urllib2.urlopen(req)
html = response.read()
soup = BeautifulSoup(html)

country = []
cou = soup.findAll('td', {"class" : "yfnc_modtitlew1"})[0].findAll(text = True)
for i in range(len(cou)):
    if ' - ' in cou[i]:
        country = cou[i].split(' -')[0]

soup.find(text = .previous.find(text = True)
'''


# combine all the result
company_result = []
for i in range(len(uniq_company_list)):
    tmp = []
    tmp.append(uniq_company_list[i])
    tmp.append(ticket_list[i])
    tmp.append("0")
    tmp.append(sector_list[i])
    tmp.append(industry_list[i])
    tmp.append(country_list[i])
    tmp.append(summary_list[i])    
    company_result.append(list(tmp))

with open('software_final.csv', 'w') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    writer.writerow(["Compnay"] + ["Ticket"] + ["MarketCap"] + ["Sector"] + ["Industry"] + ["Country"] + ["Summary"])
    for row in company_result:
        writer.writerow(row)

