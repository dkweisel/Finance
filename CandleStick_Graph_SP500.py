from matplotlib import style
import pandas as pd
import pandas_datareader.data as web
import matplotlib.pyplot as plt 
from mpl_finance import candlestick_ohlc
import matplotlib.dates as mdates
import datetime
import yfinance as yf

# style of plot
style.use('ggplot')

# SP500 (^GSPC) from yahoo finnance
'''
gspc = yf.download('^GSPC','2000-1-1')
gspc.to_csv('gspc.csv')
'''
# read csv - data pulled from yahoo finance
gspc = pd.read_csv('gspc.csv', parse_dates=True, index_col=0)
print(gspc)

# open, high, low, close
gspc_ohlc = gspc['Adj Close'].resample('10D').ohlc()
gspc_volume = gspc['Volume'].resample('10D').sum()
gspc_ohlc.reset_index(inplace=True)
gspc_ohlc['Date'] = gspc_ohlc['Date'].map(mdates.date2num)

ax1 = plt.subplot2grid((6,1), (0,0), rowspan=5, colspan=1)
ax2 = plt.subplot2grid((6,1), (5,0), rowspan=1, colspan=1, sharex=ax1)
ax1.xaxis_date()
candlestick_ohlc(ax1, gspc_ohlc.values, width=2, colorup='g')
ax2.fill_between(gspc_volume.index.map(mdates.date2num), gspc_volume.values, 0)
plt.show()
