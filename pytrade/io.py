import urllib2
import bs4
import pandas as pd
import pandas_datareader.data as web

def adj_close_ipc(start,end):

    def get_symbols(url):
        opener = urllib2.build_opener()
        opener.addheaders=[('User-agent', 'Mozilla/5.0')]
        res = opener.open(url)
        page = res.read()
        soup = bs4.BeautifulSoup(page, "lxml")
        stocks = []
        
        table = soup.find('table',{'class':"yfnc_tableout1"})


        for row in table.find_all('td', {'class':'yfnc_tabledata1'}):
            try:
                stock = row.find('a').text
                stocks.append(stock)
            except:
                pass

        return stocks

    url = 'http://finance.yahoo.com/q/cp?s=%5EMXX'

    symbols = get_symbols(url)

    data = pd.DataFrame()

    for sym in symbols:
        try:
            data[sym] = web.DataReader(sym,data_source="yahoo",
                                        start=start, end=end)['Adj Close']
        except:
            pass
            #print "Warning: ", sym, " not loaded"


    return data
    
if __name__ == '__main__':
    import datetime    
    start = datetime.date(2014,1,1)
    end = datetime.date(2016,7,7) # Year-month-day
    data = adj_close_ipc(start,end)
