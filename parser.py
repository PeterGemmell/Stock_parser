import requests
import pandas as pd
from yahoo_fin import stock_info as si
from pandas_datareader import DataReader
import numpy as np

# First we define a variable called tickers which is set
# To contain all ticker symbols in the S&P 500.

# Next the recommendations variable is set to and empty list.
# This is used to store the values we gather from the For Loop we create.

# The For Loop is accessing the Yahoo Finance page and collecting its respective recommendation
# rating.

# Finally a Pandas DataFrame is created containing each ticker and its recommendation. This is then
# downloaded in CSV format to the computer.

tickers = si.tickers_sp500()
recommendations = []

for ticker in tickers:
    lhs_url = 'https://query2.finance.yahoo.com/v10/finance/quoteSummary/'
    rhs_url = '?formatted=true&crumb=swg7qs5y9UP&lang=en-US&region=US&' \
              'modules=upgradeDowngradeHistory,recommendationTrend,' \
              'financialData,earningsHistory,earningsTrend,industryTrend&' \
              'corsDomain=finance.yahoo.com'

    url =  lhs_url + ticker + rhs_url
    r = requests.get(url)
    if not r.ok:
        recommendation = 6
    try:
        result = r.json()['quoteSummary']['result'][0]
        recommendation =result['financialData']['recommendationMean']['fmt']
    except:
        recommendation = 6

    # Added in sort so we now have the list in order with best buy's together.
    recommendations.sort()
    recommendations.append(recommendation)

    print("--------------------------------------------")
    print ("{} has an average recommendation of: ".format(ticker), recommendation)
    #time.sleep(0.5)

dataframe = pd.DataFrame(list(zip(tickers, recommendations)), columns =['Company', 'Recommendations'])
dataframe = dataframe.set_index('Company')
dataframe.to_csv('recommendations.csv')

# print (df)
