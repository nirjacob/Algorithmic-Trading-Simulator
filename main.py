from result_tracker import stock_bought, num_of_stocks, total_money_spent
# from momentum_algorithm import hqm_dataframe_results
import streamlit as st
import numpy as np
from sp500EqualWeight import final_dataframe
import time

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


# api_url = f'https://sandbox.iexapis.com/stable/stock/{symbol}/quote/?token={IEX_CLOUD_API_TOKEN}'
# updated_price = requests.get(api_url).json()
# stock_price = data['latestPrice']

last_rows = np.random.randn(1, 1)
chart = st.line_chart(last_rows)

for i in range(1, 101):
    new_rows = last_rows[-1, :] + np.random.randn(5, 1).cumsum(axis=0)
    chart.add_rows(new_rows)
    last_rows = new_rows
    time.sleep(0.5)
