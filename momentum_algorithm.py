from statistics import mean
import numpy as np
import pandas as pd
import requests
import math
from scipy import stats
stocks = pd.read_csv('/app/botofwallstreet/sp_500_stocks.csv')
IEX_CLOUD_API_TOKEN = 'Tpk_059b97af715d417d9f49f50b51b1c448'
portfolio_size = 100000


def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


symbol_groups = list(chunks(stocks['Ticker'], 100))
symbol_strings = []
for i in range(0, len(symbol_groups)):
    symbol_strings.append(','.join(symbol_groups[i]))

hqm_columns = [
    'Ticker',
    'Price',
    'Number of Shares to Buy',
    'Total Price',
    'One-Year Price Return',
    'One-Year Return Percentile',
    'Six-Month Price Return',
    'Six-Month Return Percentile',
    'Three-Month Price Return',
    'Three-Month Return Percentile',
    'One-Month Price Return',
    'One-Month Return Percentile',
    'HQM Score'
]

hqm_dataframe = pd.DataFrame(columns=hqm_columns)
for symbol_string in symbol_strings:
    batch_api_call_url = f'https://sandbox.iexapis.com/stable/stock/market/batch/?types=stats,quote&symbols={symbol_string}&token={IEX_CLOUD_API_TOKEN}'
    data = requests.get(batch_api_call_url).json()
    for symbol in symbol_string.split(','):
        hqm_dataframe = hqm_dataframe.append(
            pd.Series([symbol,
                       data[symbol]['quote']['latestPrice'],
                       'N/A',
                       'N/A',
                       data[symbol]['stats']['year1ChangePercent'],
                       'N/A',
                       data[symbol]['stats']['month6ChangePercent'],
                       'N/A',
                       data[symbol]['stats']['month3ChangePercent'],
                       'N/A',
                       data[symbol]['stats']['month1ChangePercent'],
                       'N/A',
                       'N/A'
                       ],
                      index=hqm_columns),
            ignore_index=True)

time_periods = [
    'One-Year',
    'Six-Month',
    'Three-Month',
    'One-Month'
]
# zero out the data frame so "percentile of score" function can calculate values properly
for row in hqm_dataframe.index:
    for time_period in time_periods:
        if hqm_dataframe.loc[row, f'{time_period} Price Return'] == None:
            hqm_dataframe.loc[row, f'{time_period} Price Return'] = 0

for row in hqm_dataframe.index:
    for time_period in time_periods:
        change_col = f'{time_period} Price Return'
        percentile_col = f'{time_period} Return Percentile'
        hqm_dataframe.loc[row, percentile_col] = percentileofscore(
            hqm_dataframe[change_col], hqm_dataframe.loc[row, change_col])

for row in hqm_dataframe.index:
    momentum_percentiles = []
    for time_period in time_periods:
        momentum_percentiles.append(
            hqm_dataframe.loc[row, f'{time_period} Return Percentile'])
    hqm_dataframe.loc[row, 'HQM Score'] = mean(momentum_percentiles)

hqm_dataframe.sort_values(by='HQM Score', ascending=False, inplace=True)
hqm_dataframe = hqm_dataframe[:10]
hqm_dataframe.reset_index(inplace=True, drop=True)
position_size = portfolio_size / len(hqm_dataframe.index)
for i in range(0, 10):
    hqm_dataframe.loc[i,
                      'Number of Shares to Buy'] = int(position_size // hqm_dataframe['Price'][i])
    hqm_dataframe.loc[i,
                      'Total Price'] = int((hqm_dataframe.loc[i, 'Number of Shares to Buy']) * (hqm_dataframe['Price'][i]))


hqm_dataframe['Number of Shares Bought'] = hqm_dataframe['Number of Shares to Buy']

hqm_dataframe_results = hqm_dataframe[[
    'Ticker', 'HQM Score', 'Number of Shares Bought', 'Price', 'Total Price']]
