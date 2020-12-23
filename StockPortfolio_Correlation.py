import bs4 as bs
from os import read
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 
import matplotlib.dates as mdates
from matplotlib import style
import pandas_datareader.data as web
import datetime as dt
import yfinance as yf

style.use('ggplot')

'''
# SP500 list of companies from wiki
table=pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
sp500_co = table[0]
sp500_co.to_csv('S&P500-Info.csv')
sp500_co.to_csv("S&P500-Symbols.csv", columns=['Symbol'])
print(sp500_co)
'''
# Portfolio Analysis #
###################### 

# portfolio of stocks - FAANG
portfolio = ['AAPL', 'AMZN', 'FB', 'NFLX', 'GOOG', 'GOOGL']
data = yf.download(portfolio,'2015-1-1')['Adj Close']
# calculates daily return 


daily_return = (data/data.shift(1)) - 1
# drops NA values
data.dropna(inplace=True) 

print(data)
print(daily_return)
#info_tech_data['AAPL'].plot()
#plt.show()

# correlation values of daily returns
corr = daily_return.corr()
print(corr)

# creation of heatmap
data = corr.values
fig = plt.figure()
ax = fig.add_subplot(1,1,1)

heatmap = ax.pcolor(data, cmap=plt.cm.RdYlGn)
fig.colorbar(heatmap)
ax.set_xticks(np.arange(data.shape[0]) + 0.5, minor=False)
ax.set_yticks(np.arange(data.shape[1]) + 0.5, minor=False)
ax.invert_yaxis()
ax.xaxis.tick_top()

column_labels = corr.columns
row_labels = corr.index

ax.set_xticklabels(column_labels)
ax.set_yticklabels(row_labels)
plt.xticks(rotation=90)
heatmap.set_clim(-1,1)
plt.tight_layout()
plt.show()
