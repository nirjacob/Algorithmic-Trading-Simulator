from result_tracker import stock_bought, num_of_stocks, total_money_spent
from momentum_algorithm import hqm_dataframe_results
import streamlit as st
import numpy as np
from sp500EqualWeight import final_dataframe
import time
import requests
import pandas as pd
portfolio_size = 1000000
IEX_CLOUD_API_TOKEN = 'Tpk_059b97af715d417d9f49f50b51b1c448'

selected_algorithm = st.selectbox('Select Trading Algorithm', [
                                  'Quantitative Momentum', 'Quantitative Value'])

start = st.button('Start Trading Simulation')

if start:
    st.subheader("Top Ranked Stocks")
    if selected_algorithm == 'Quantitative Momentum':
        st.write(hqm_dataframe_results)
    # else
    #     st.write(value_dataframe_results)


def updated_results():
    owned_stock_prices = 0
    latest_price = 0
    for i in range(0, 9):
        api_url = f'https://sandbox.iexapis.com/stable/stock/{stock_bought[i]}/quote/?token={IEX_CLOUD_API_TOKEN}'
        data = requests.get(api_url).json()
        latest_price = int(data['latestPrice'])
        owned_stock_prices += (latest_price * num_of_stocks[i])
    return (owned_stock_prices - total_money_spent)


st.subheader("Algorithm Real-Time Results")
if start and selected_algorithm == 'Quantitative Momentum':
    gains = updated_results()
    prices_array = np.array([gains])
    result_chart = st.line_chart(prices_array)
    for i in range(0, 20):
        new_rows = np.append(prices_array, updated_results())
        result_chart.add_rows(new_rows)
        prices_array = new_rows
        time.sleep(5)
elif start == False:
    st.info('Please choose trading algorithm and enter Portfolio size')
# elif start and portfolio_size and selected_algorithm == 'Quantitative Value':
    # value_algo
