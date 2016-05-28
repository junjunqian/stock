import csv as csv
from csv import DictReader
import re
import pandas as pd
from bs4 import BeautifulSoup
import urllib.request as urllib2

# read the table, without header
yahoo = csv.reader(open('software_final.csv'))
company_ticket_list=[]
company_list=[]
sector_list=[]
industry_list=[]
country_list=[]
summary_list=[]

header = next(yahoo)
for row in yahoo:
    company_ticket = row[1]
    if company_ticket != '':
        company_ticket_list.append(company_ticket)
    company = row[0]
    company_list.append(company)
    sector = row[3]
    sector_list.append(sector)    
    industry = row[4]
    industry_list.append(industry)
    country = row[5]
    country_list.append(country)    
    summary = row[6]
    summary_list.append(summary)


# get url list
url_preifx = "http://finance.yahoo.com/q?s="
acturalurl=[]
for i in company_ticket_list:
    actural = url_preifx + i
    acturalurl.append(actural)

marketcap_list = []
for i in range(len(company_ticket_list)):
    req = urllib2.Request(acturalurl[i])
    response = urllib2.urlopen(req)
    html = response.read()
    soup = BeautifulSoup(html)
    try: 
        marketcap = soup.find(text='Market Cap:').next.find(text=True)
    except:
        marketcap = ' '
    marketcap_list.append(marketcap)
    print (len(marketcap_list))

company_result = []
for i in range(len(company_ticket_list)):
    tmp = []
    tmp.append(company_list[i])
    tmp.append(company_ticket_list[i])
    tmp.append(marketcap_list[i])
    tmp.append(sector_list[i])
    tmp.append(industry_list[i])
    tmp.append(country_list[i])
    tmp.append(summary_list[i])    
    company_result.append(list(tmp))

with open('software_final.csv2.csv', 'w') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    writer.writerow(["Compnay"] + ["Ticket"] + ["MarketCap"] + ["Sector"] + ["Industry"] + ["Country"] + ["Summary"])
    for row in company_result:
        writer.writerow(row)

    


