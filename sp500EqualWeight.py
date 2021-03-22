# python ms-python formatter
import math
import xlsxwriter
import requests
import pandas as pd
import numpy as np
import streamlit as st
IEX_CLOUD_API_TOKEN = 'Tpk_059b97af715d417d9f49f50b51b1c448'
# from secrets import IEX_CLOUD_API_TOKEN
stocks = pd.read_csv(
    'file:///C:/Users/Nir/Desktop/TradingAlgProject/BotOfWallStreet-1/sp_500_stocks.csv')
symbol = 'AAPL'

# VV this is an f string(the {symbol} replaced by the var synbol)
api_url = f'https://sandbox.iexapis.com/stable/stock/{symbol}/quote/?token={IEX_CLOUD_API_TOKEN}'
data = requests.get(api_url).json()
stock_price = data['latestPrice']
market_cap = data['marketCap']

# building a pandas data frame of all the sotcks
# data frame contains columns for each stock of: ticker,stock price, market cap, num of shares to buy
my_columns = ['Ticker', 'Stock Price',
              'Market Capitalization', 'Number of Shares to Buy']
final_dataframe = pd.DataFrame(columns=my_columns)
final_dataframe = pd.DataFrame(columns=my_columns)
# iterate on the names from the sp_500_stocks.csv and use them to make API requests
for stock in stocks['Ticker'][:5]:
    api_url = f'https://sandbox.iexapis.com/stable/stock/{stock}/quote/?token={IEX_CLOUD_API_TOKEN}'
    data = requests.get(api_url).json()
# pandas dataframe can append panda dataframe only
# so we create a pandas Series that is acceptable and it accepts a python list!
    final_dataframe = final_dataframe.append(
        pd.Series(
            [
                stock,
                data['latestPrice'],
                data['marketCap'],
                'N/A'
            ], index=my_columns),
        ignore_index=True
    )

# batch API
# Function sourced from
# https://stackoverflow.com/questions/312443/how-do-you-split-a-list-into-evenly-sized-chunks


def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


symbol_strings = []
symbol_groups = list(chunks(stocks['Ticker'], 100))
# need to update this to 5 for total stocks
for i in range(0, len(symbol_groups))[0:1]:
    symbol_strings.append(','.join(symbol_groups[i]))

for symbol_string in symbol_strings:
    batch_api_call_url = f'https://sandbox.iexapis.com/stable/stock/market/batch?symbols={symbol_string},fb,tsla&types=quote,news,chart&token={IEX_CLOUD_API_TOKEN}'
    data = requests.get(batch_api_call_url).json()
    for symbol in symbol_string.split(','):
        final_dataframe = final_dataframe.append(
            pd.Series(
                [
                    symbol,
                    data[symbol]['quote']['latestPrice'],
                    data[symbol]['quote']['marketCap'],
                    'N/A'
                ],
                index=my_columns),
            ignore_index=True
        )

protfolio_size = 250000
val = float(protfolio_size)
position_size = val/len(final_dataframe.index)
number_of_apple_shares = math.floor(position_size/500)

for i in range(0, len(final_dataframe.index)):
    final_dataframe.loc[i, 'Number of Shares to Buy'] = math.floor(
        position_size/final_dataframe.loc[i, 'Stock Price'])
