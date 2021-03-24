from result_tracker import stock_bought, num_of_stocks, total_money_spent
from momentum_algorithm import hqm_dataframe_results
import streamlit as st
import numpy as np
from sp500EqualWeight import final_dataframe
import time
import requests
import pandas as pd

IEX_CLOUD_API_TOKEN = 'Tpk_059b97af715d417d9f49f50b51b1c448'

top_col1, top_col2 = st.beta_columns(2)
with top_col1:
    selected_algorithm = st.selectbox('Select Trading Algorithm', [
        'Quantitative Momentum', 'Quantitative Value'])
with top_col2:
    portfolio_size = st.number_input('Enter Portfolio Size')

start = st.button('Start Trading Simulation')

if start and portfolio_size:
    st.subheader("Top 10 Stocks to Buy")
    st.write(final_dataframe)


st.subheader("Trading Results")
fake_results = np.random.randn(10, 1)
if start and portfolio_size:
    st.line_chart(fake_results)
elif start and portfolio_size == 0:
    st.error('Enter Portfolio Size')
elif start == False:
    st.info('Please choose trading algorithm and enter Portfolio size')


def updated_price():
    owned_stock_prices = 0
    latest_price = 0
    for i in range(1, 10):
        api_url = f'https://sandbox.iexapis.com/stable/stock/{stock_bought[i]}/quote/?token={IEX_CLOUD_API_TOKEN}'
        data = requests.get(api_url).json()
        latest_price = int(data['latestPrice'])
        owned_stock_prices += latest_price * num_of_stocks[i]
    return owned_stock_prices - total_money_spent


gains = updated_price()
prices_array = np.array([gains])

# chart_data = pd.DataFrame(
#     prices_array,
#     columns=['Gains'])

result_chart = st.line_chart(prices_array)

for i in range(1, 10):
    new_rows = prices_array.append(updated_price())
    result_chart.add_rows(new_rows)
    prices_array = new_rows
    time.sleep(5)


# first_row = {'Profit/Loss': [gains]}
# chart_data = pd.DataFrame(data=first_row)
# result_chart = st.line_chart(chart_data)

# for i in range(1, 10):
#     new_rows = chart_data + {'Profit/Loss': [updated_price()]}
#     result_chart.add_rows(new_rows)
#     chart_data = new_rows
#     time.sleep(15)
