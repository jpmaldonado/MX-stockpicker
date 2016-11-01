# -*- coding: utf-8 -*-
"""
Created on Mon May 02 05:05:36 2016

@author: Pablo
"""
import pandas as pd
from pandas_datareader import data as web  # data retrieval
import requests, bs4
import sqlite3
import datetime
from _config import TICKSDB


def get_symbols(url):
    res = requests.get(url)
    soup = bs4.BeautifulSoup(res.text, "lxml")
    stocks = []
    table = soup.find('table', {'class':'yfnc_tableout1'})

    for row in table.find_all('td', {'class':'yfnc_tabledata1'}):
        try:
            stock = row.find('a').text
            stocks.append(stock)
        except:
            pass

    return stocks


url = 'https://uk.finance.yahoo.com/q/cp?s=%5EMXX'

symbols = get_symbols(url)

data = pd.DataFrame()

start = datetime.datetime(2015,1,1)
today = datetime.datetime.now().strftime('%Y-%m-%d')


conn = sqlite3.connect(TICKSDB)
## Store daily data
for sym in symbols:
    try:
        new_data = web.DataReader(sym,data_source="yahoo", start=start, end=today)
        parsed_sym = sym.split('.')[0]
        new_data.to_sql(parsed_sym,conn, if_exists='append')

        # Store closing prices separately
        data[sym] = web.DataReader(sym,data_source="yahoo")['Adj Close']
    except:
        pass

data.dropna(inplace=True)
data.to_sql('adjclose', conn, if_exists="append") 
conn.close()
