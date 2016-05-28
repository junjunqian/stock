# convert the yahoo api marketcap to real number
import csv as csv
from csv import DictReader
import re
import pandas as pd
from bs4 import BeautifulSoup
import urllib.request as urllib2

yahoo = csv.reader(open('software_final.csv'))
company_list=[]
company_ticket_list=[]
marketcap_list = []
sector_list=[]
industry_list=[]
country_list=[]
summary_list=[]
header = next(yahoo)

for row in yahoo:
    company = row[0]
    company_list.append(company)
    company_ticket = row[1]
    company_ticket_list.append(company_ticket)
    marketcap = row[2]
    marketcap_list.append(marketcap)
    sector = row[3]
    sector_list.append(sector)    
    industry = row[4]
    industry_list.append(industry)
    country = row[5]
    country_list.append(country)    
    summary = row[6]
    summary_list.append(summary)

convert=[]
for i in marketcap_list:
    if 'K' in i:
        marketcap = float(i.split('K')[0]) * 1000
    elif 'M' in i:
        marketcap = float(i.split('M')[0]) * 1000000
    elif 'B' in i:
        marketcap = float(i.split('B')[0]) * 1000000000
    convert.append(marketcap)

company_result = []
for i in range(len(company_ticket_list)):
    tmp = []
    tmp.append(company_list[i])
    tmp.append(company_ticket_list[i])
    tmp.append(convert[i])
    tmp.append(sector_list[i])
    tmp.append(industry_list[i])
    tmp.append(country_list[i])
    tmp.append(summary_list[i])    
    company_result.append(list(tmp))

with open('software_final2.csv', 'w') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    writer.writerow(["Compnay"] + ["Ticket"] + ["MarketCap"] + ["Sector"] + ["Industry"] + ["Country"] + ["Summary"])
    for row in company_result:
        writer.writerow(row)




