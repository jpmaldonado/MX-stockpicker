## Returns major portfolio statistics for an input of weights vector/array

import numpy as np
import datetime

###############################################################################
##### Cross-sectional mean reversion
###############################################################################

def xsection_mean_reversion_portfolio(data):
    data = data.tail()
    rets = np.log(data/data.shift(1))
    xrets = np.nanmean(rets, axis=0)
    xmean = np.nanmean(xrets)

    normalize = np.sum([abs(xrets[idx]-xmean) for idx in range(len(xrets))])
    weights = [-(xrets[idx]-xmean)/normalize for idx in range(len(xrets))]

###            THIS NEEDS TO BE MODIFIED!!! IT DOES NOT MAKE SENSE
    def statistics(weights):
        weights = np.array(weights)
        # Expected portfolio return
        pret = np.sum(rets.mean()*weights)*252

        # Expected portfolio volatility
        pvol = np.sqrt(np.dot(weights.T, np.dot(rets.cov()*252,weights)))

        # Sharpe ratio for rf=0: pret/pvol
        return np.array([pret, pvol, pret/pvol])

    return zip(data.columns,weights), statistics(weights)

###############################################################################
#### Max Sharpe ratio portfolio
###############################################################################

def max_sharpe_portfolio(data):
    ''' Data is the dataframe consisting of adj close prices'''

    n_symbols= data.shape[1]

    # Calculation of log returns
    rets = np.log(data/data.shift(1))

    # Annualized average log returns
    rets.mean()*252


    def statistics(weights):
        weights = np.array(weights)
        # Expected portfolio return
        pret = np.sum(rets.mean()*weights)*252

        # Expected portfolio volatility
        pvol = np.sqrt(np.dot(weights.T, np.dot(rets.cov()*252,weights)))

        # Sharpe ratio for rf=0: pret/pvol
        return np.array([pret, pvol, pret/pvol])


    import scipy.optimize as sco

    ## Max-sharpe portfolio
    def min_func_sharpe(weights):
        return -statistics(weights)[2]

    cons = ({'type':'eq', 'fun':lambda x: np.sum(x)-1})
    bnds = tuple((0,1) for x in range(n_symbols))


    opts = sco.minimize(min_func_sharpe, n_symbols*[1./n_symbols,],
                        method = 'SLSQP', bounds=bnds, constraints = cons)


    decision = opts['x'].round(3)

    # Return, volatility and Sharpe ratio
    metrics = statistics(opts['x']).round(3)

    out = zip(data.columns.values,decision)

    return out, metrics

