###############################################################################
#### Backtest
###############################################################################
import pandas as pd
import numpy as np
import datetime
from pytrade.io import adj_close_ipc

def pf_backtest(numdays, pf,start):
        ## Backtesting
    yday = datetime.datetime.today()-datetime.timedelta(days=1)
    base = yday-datetime.timedelta(days=numdays)

    test_dates = pd.bdate_range(base,yday)
    test_end = max(test_dates)
    test_start = min(test_dates)

    test_data = adj_close_ipc(start,test_end)


    rets = []
    metrics = []

    #test_dates = [d+datetime.timedelta(days=1) for d in test_dates]

    for date in test_dates:
        test = test_data[start:date-datetime.timedelta(days=1)]
        val = test_data[date:date]
        portfolio, mt = pf(test)

        metrics.append(mt)

        ret = 0.0

        for row in portfolio:
            try:
                previous_close = test[row[0]].tail()[-1]
                current_close = val[row[0]][0]
                temp = row[1]*np.log(current_close/previous_close)
                if np.isnan(temp):
                    #print "NaN here: ", row
                    ret += 0.0
                else:
                    ret += temp
            except:
                pass

        rets.append(ret)

    # Ba
    bt = test_data[test_start:test_end]
    market_rets = np.nansum(np.log(bt.values/bt.shift(1).values), axis = 1)


    test_dates = [pd.Timestamp(x) for x in test_dates]
    df = pd.DataFrame(index=test_dates)
    df['Strategy'] = rets
    df['Market'] = market_rets
    df['Portfolio Return'] = [m[0] for m in metrics]
    df['Portfolio Volatility'] = [m[1] for m in metrics]
    df['Sharpe Ratio'] = [m[2] for m in metrics]
    return df
