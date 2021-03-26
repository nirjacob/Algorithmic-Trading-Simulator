from value_result_tracker import stock_bought_value, num_of_stocks_value, total_money_spent_value
from value_algorithm import rv_dataframe_results
from momentum_algorithm import hqm_dataframe_results
from momentum_result_tracker import stock_bought, num_of_stocks, total_money_spent
import streamlit as st
import numpy as np
import time
import requests
import pandas as pd

portfolio_size = 100000
start = False
IEX_CLOUD_API_TOKEN = 'Tpk_059b97af715d417d9f49f50b51b1c448'

title_placeholder = st.empty()
title_placeholder.header("Welcome to my trading algorithm simulation!")
placeholder = st.empty()
placeholder.text(
    "There are two algorithm profiles - momentum and value based.\nThe default portfolio size is set to 100,000$")


selected_algorithm = st.selectbox('Select Trading Algorithm', [
                                  'Quantitative Momentum', 'Quantitative Value'])

start = st.button('Start Trading Simulation')
if start:
    placeholder.empty()
    title_placeholder.empty()
    st.header("Top Ranked Stocks")
    if selected_algorithm == 'Quantitative Momentum':
        st.write(hqm_dataframe_results)
    else:
        st.write(rv_dataframe_results)

flag = False


def updated_results(shares_ammount, shares_bought, total_investment):
    owned_stock_prices = 0
    latest_price = 0
    for i in range(0, 10):
        api_url = f'https://sandbox.iexapis.com/stable/stock/{shares_bought[i]}/quote/?token={IEX_CLOUD_API_TOKEN}'
        data = requests.get(api_url).json()
        latest_price = int(data['latestPrice'])
        owned_stock_prices += (latest_price * shares_ammount[i])
    if (owned_stock_prices - total_investment) > 0 and flag = False:
        st.balloons()
        st.success('Congratulation! You Have Beaten The Market!')
        flag = True
    return (owned_stock_prices - total_investment)


st.header("Algorithm Real-Time Results")
if start and selected_algorithm == 'Quantitative Momentum':
    gains = updated_results(num_of_stocks, stock_bought, total_money_spent)
    prices_array = np.array([gains])
    with st.beta_container():
        result_chart = st.line_chart(prices_array)
        st.write("Profit/Loss (Ticks Every 2 seconds)")
    balance_placeholder = st.empty()
    for i in range(0, 30):
        new_rows = np.append(prices_array, updated_results(
            num_of_stocks, stock_bought, total_money_spent))
        result_chart.add_rows(new_rows)
        prices_array = new_rows
        time.sleep(0.5)
        balance_placeholder.empty()
        balance_placeholder.write(f"Previous recorded balance: {new_rows[i]}💲")
elif start == False:
    st.info('Please choose trading algorithm and start the simulation')
elif start and portfolio_size and selected_algorithm == 'Quantitative Value':
    gains = updated_results(num_of_stocks_value,
                            stock_bought_value, total_money_spent_value)
    prices_array = np.array([gains])
    with st.beta_container():
        result_chart = st.line_chart(prices_array)
        st.write("Profit/Loss (Ticks Every 2 seconds)")
    balance_placeholder = st.empty()
    for i in range(0, 30):
        new_rows = np.append(prices_array, updated_results(
            num_of_stocks_value, stock_bought_value, total_money_spent_value))
        result_chart.add_rows(new_rows)
        prices_array = new_rows
        time.sleep(0.5)
        balance_placeholder.empty()
        balance_placeholder.write(f"Previous recorded balance: {new_rows[i]}💲")

st.info('For more info on this app, see readme file at https://github.com/nirjacob/BotOfWallStreet')
