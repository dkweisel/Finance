from matplotlib import lines
import pandas as pd
from pandas.core import groupby
import pandas_datareader.data as web
import matplotlib.pyplot as plt 
import datetime

'''
The S&P 500 index (SPX) tracks the performance of 500 of the largest companies listed on 
US exchanges, such as the New York Stock Exchange (NYSE) and Nasdaq. The S&P 500, also known as the US 500, 
can be used as a live indicator for the strength of US equities. Follow the S&P 500 price using the real-time chart and 
stay up to date with the latest S&P 500 forecast, news and analysis articles.

The S&P 500 is considered an effective representation for the economy due to its inclusion of around 500 companies, which covers all 
areas of the United States and across all industries. In contrast, the Dow Jones Industrial Average (DJIA) is comprised of 30 companies, 
leading to a more narrow reflection. Further, the DJIA is a price-weighted index, so the largest weighted components are determined by its stock 
price rather than some fundamental measure.7﻿

The S&P 500 is a broader representation, having more stocks and covering every industry. 
The DJIA is limited and the movement of a stock in the DJIA can have a greater impact than that of the S&P 500. 
The largest weighted stock in the S&P 500 likely has a smaller weighting than the largest weighted stock in the DJIA. 
The movement of a few companies can have a profound impact on the DJIA.

df = pd.read_csv(r'/Users/deannaweisel/Documents/Visual_Studios/US_covidcases_transposed.csv')
us_count = df.sum(numeric_only=True)
# Pull from file
sp500 = pd.read_csv(r'/Users/deannaweisel/Documents/Visual_Studios/SP500.csv')

def add_returns(inp_data):
    inp_data["Return"] = (inp_data["Close"] / inp_data["Open"]) - 1

add_returns(sp500)

print(sp500.info())
print(sp500[['Date', 'Return']])

'''
# analysis of SP500(FRED) and COVID19(John Hopkins) data 
# pull from internet - FRED
start = datetime.datetime(2020, 1, 1)
end = datetime.datetime(2020, 12, 31)

fredSP500 = web.DataReader('SP500', 'fred', start, end)

# determines daily return
fredSP500['daily_return'] = (fredSP500['SP500']/ fredSP500['SP500'].shift(1)) -1
fredSP500.dropna(inplace = True) # removes NaN values
print(fredSP500['daily_return'])

# close price of SP500 from FRED
close = fredSP500['SP500']

# plot of daily return 
plt.plot(fredSP500['daily_return'], label ='Daily Return')
plt.legend()
plt.title('S&P500 Daily Returns', fontsize=12)
plt.xlabel('DATE', fontsize=10)
plt.ylabel('Daily Return', fontsize=10)
plt.grid(which="major", color='k', linestyle='-.', linewidth=0.5)
plt.show()

# covid analysis - confirmed cases count 
df = pd.read_csv(r'/Users/deannaweisel/Documents/Visual_Studios/US_covidcases_transposed.csv', parse_dates=True)
us_count = df.sum(numeric_only=True)
us_count.index = pd.to_datetime(us_count.index)

df_corr= df.corr()
print



# comparative plot of US counts vs SP500 close
us_count.plot(label='US Count of Confirmed Cases', color='ForestGreen')
close.plot(secondary_y=True, label='S&P 500 Close')

plt.legend()
plt.title('Comparative Analysis of COVID-19 and Impact on S&P 500', fontsize=12)
plt.xlabel('DATE', fontsize=10)
plt.ylabel('Close Price', fontsize=10)
plt.grid(which="major", color='k', linestyle='-.', linewidth=0.5)
plt.axvline(x="2020-03-01", color='gold', linestyle='-.', linewidth=0.7)
plt.axvline(x="2020-04-01", color='gold', linestyle='-.', linewidth=0.7)
plt.show()

# moving average of close price of SP500
ma_5 = close.rolling(5).mean()
ma_10 = close.rolling(10).mean()
ma_30 = close.rolling(30).mean()

plt.plot(close, label ='S&P 500')
plt.plot(ma_5,label = 'MA 5 days')
plt.plot(ma_10,label = 'MA 10 days')
plt.plot(ma_30,label = 'MA 30 days')

plt.legend()
plt.title('S&P 500 Moving Average of Close Price', fontsize=12)
plt.xlabel('DATE', fontsize=10)
plt.ylabel('Close Price', fontsize=10)
plt.grid(which="major", color='k', linestyle='-.', linewidth=0.5)
plt.show()

# plt.figure(figsize=(15,10))
