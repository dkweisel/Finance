from matplotlib import lines
import pandas as pd
from pandas.core import groupby
import pandas_datareader.data as web
import matplotlib.pyplot as plt 
import datetime
import yfinance as yf

'''
# SP500 list of companies from wiki
table=pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
sp500_co = table[0]
sp500_co.to_csv('S&P500-Info.csv')
sp500_co.to_csv("S&P500-Symbols.csv", columns=['Symbol'])
print(sp500_co)

sector = sp500_co['GICS Sector']
print(sector)
by_sector = (sp500_co.groupby("GICS Sector")['Symbol'])
print(by_sector)
'''
# individual performing stocks, bonds, ETFs 
bonds_SP500 = ['^GSPC', 'VBTLX', 'VBLAX', 'VTEAX'] 
info_tech = ['AAPL', 'ADBE', 'CRM', 'INTC', 'MA', 'MSFT', 'NVDA', 'PYPL', 'V']
health_care = ['JNJ', 'MRK', 'UNH']
financials = ['BRK-B', 'JPM']
com_services = ['CMCSA', 'DIS', 'FB', 'GOOG', 'GOOGL', 'NFLX', 'T', 'VZ']
consumer_dis = ['AMZN', 'HD']
consumer_staples = ['PG']

# fetching data
gspc = yf.download(bonds_SP500,'2020-1-1')['Adj Close']
info_tech_data = yf.download(info_tech,'2020-1-1')['Adj Close']
health_care_data = yf.download(health_care,'2020-1-1')['Adj Close']
financials_data = yf.download(financials,'2020-1-1')['Adj Close']
com_services_data = yf.download(com_services, '2020-1-1')['Adj Close']
consumer_dis_data = yf.download(consumer_dis, '2020-1-1')['Adj Close']
consumer_staples_data = yf.download(consumer_staples, '2020-1-1')['Adj Close']

# plotting of sector returns
((info_tech_data.pct_change()+1).cumprod()).plot(figsize=(10, 7))
plt.legend()
plt.title("Information Technology Sector:  2020 Returns", fontsize=12)
plt.ylabel('Cumulative Returns', fontsize=10)
plt.xlabel('DATE', fontsize=10)
plt.grid(which="major", color='k', linestyle='-.', linewidth=0.5)
plt.show()

((com_services_data.pct_change()+1).cumprod()).plot(figsize=(10, 7))
plt.legend()
plt.title("Communication Services Sector:  2020 Returns", fontsize=12)
plt.ylabel('Cumulative Returns', fontsize=10)
plt.xlabel('DATE', fontsize=10)
plt.grid(which="major", color='k', linestyle='-.', linewidth=0.5)
plt.show()

((health_care_data.pct_change()+1).cumprod()).plot(figsize=(10, 7))
plt.legend()
plt.title("Health Care Sector:  2020 Returns", fontsize=12)
plt.ylabel('Cumulative Returns', fontsize=10)
plt.xlabel('DATE', fontsize=10)
plt.grid(which="major", color='k', linestyle='-.', linewidth=0.5)
plt.show()

((gspc.pct_change()+1).cumprod()).plot(figsize=(10, 7))
plt.legend()
plt.title('S&P 500 v Bond ETFs: 2020 Daily Returns', fontsize=12)
plt.xlabel('DATE', fontsize=10)
plt.ylabel('Daily Return', fontsize=10)
plt.grid(which="major", color='k', linestyle='-.', linewidth=0.5)
plt.show()

#print(data.head())

'''
 10/20 are the twenty-five largest S&P 500 index constituents by weight:3﻿
AAPL:Apple Inc.
ADBE:Adobe Inc.
AMZN:Amazon.com Inc.
BRK-B:Berkshire Hathaway
CMCSA:Comcast Corp.
CRM:Salesforce.com
DIS:The Walt Disney Company
FB:Facebook, Inc.
GOOG:Alphabet Inc. (Class C)
GOOGL:Alphabet Inc. (Class A)
HD:Home Depot
INTC:Intel Corp.
JNJ:Johnson & Johnson
JPM:JPMorgan Chase & Co.
MA:Mastercard Inc.
MRK:Merck & Co.
MSFT:Microsoft Corp.
NFLX:Netflix Inc.
NVDA:Nvidia Corporation
PG:Procter & Gamble
PYPL:PayPal
T:AT&T Inc.
UNH:UnitedHealth Group Inc.
V:Visa Inc.
VZ:Verizon Communications
'''
