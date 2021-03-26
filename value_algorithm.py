from statistics import mean
import numpy as np
import pandas as pd
import requests
import math
from scipy.stats import percentileofscore as score

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

rv_columns = [
    'Ticker',
    'Price',
    'Number of Shares to Buy',
    'Price-to-Earnings Ratio',
    'PE Percentile',
    'Price-to-Book Ratio',
    'PB Percentile',
    'Price-to-Sales Ratio',
    'PS Percentile',
    'EV/EBITDA',
    'EV/EBITDA Percentile',
    'EV/GP',
    'EV/GP Percentile',
    'RV Score'
]

rv_dataframe = pd.DataFrame(columns=rv_columns)

for symbol_string in symbol_strings:
    batch_api_call_url = f'https://sandbox.iexapis.com/stable/stock/market/batch?symbols={symbol_string}&types=quote,advanced-stats&token={IEX_CLOUD_API_TOKEN}'
    data = requests.get(batch_api_call_url).json()
    for symbol in symbol_string.split(','):
        enterprise_value = data[symbol]['advanced-stats']['enterpriseValue']
        ebitda = data[symbol]['advanced-stats']['EBITDA']
        gross_profit = data[symbol]['advanced-stats']['grossProfit']

        try:
            ev_to_ebitda = enterprise_value/ebitda
        except TypeError:
            ev_to_ebitda = np.NaN

        try:
            ev_to_gross_profit = enterprise_value/gross_profit
        except TypeError:
            ev_to_gross_profit = np.NaN

        rv_dataframe = rv_dataframe.append(
            pd.Series([
                symbol,
                data[symbol]['quote']['latestPrice'],
                'N/A',
                data[symbol]['quote']['peRatio'],
                'N/A',
                data[symbol]['advanced-stats']['priceToBook'],
                'N/A',
                data[symbol]['advanced-stats']['priceToSales'],
                'N/A',
                ev_to_ebitda,
                'N/A',
                ev_to_gross_profit,
                'N/A',
                'N/A'
            ],
                index=rv_columns),
            ignore_index=True
        )

rv_dataframe[rv_dataframe.isnull().any(axis=1)]
for column in ['Price-to-Earnings Ratio', 'Price-to-Book Ratio', 'Price-to-Sales Ratio',  'EV/EBITDA', 'EV/GP']:
    rv_dataframe[column].fillna(rv_dataframe[column].mean(), inplace=True)
rv_dataframe[rv_dataframe.isnull().any(axis=1)]
metrics = {
    'Price-to-Earnings Ratio': 'PE Percentile',
    'Price-to-Book Ratio': 'PB Percentile',
    'Price-to-Sales Ratio': 'PS Percentile',
    'EV/EBITDA': 'EV/EBITDA Percentile',
    'EV/GP': 'EV/GP Percentile'
}

for row in rv_dataframe.index:
    for metric in metrics.keys():
        rv_dataframe.loc[row, metrics[metric]] = score(
            rv_dataframe[metric], rv_dataframe.loc[row, metric])/100

for row in rv_dataframe.index:
    value_percentiles = []
    for metric in metrics.keys():
        value_percentiles.append(rv_dataframe.loc[row, metrics[metric]])
    rv_dataframe.loc[row, 'RV Score'] = mean(value_percentiles)
rv_dataframe.sort_values(by='RV Score', ascending=False, inplace=True)
rv_dataframe = rv_dataframe[:10]
rv_dataframe.reset_index(drop=True, inplace=True)
position_size = (portfolio_size) / len(rv_dataframe.index)
for i in range(0, 10):
    rv_dataframe.loc[i, 'Number of Shares to Buy'] = int(
        position_size // rv_dataframe['Price'][i])
    rv_dataframe.loc[i, 'Total Price'] = int(
        (rv_dataframe.loc[i, 'Number of Shares to Buy']) * (rv_dataframe['Price'][i]))

rv_dataframe['Number of Shares Bought'] = rv_dataframe['Number of Shares to Buy']

rv_dataframe_results = rv_dataframe[[
    'Ticker', 'RV Score', 'Number of Shares Bought', 'Price', 'Total Price']]
