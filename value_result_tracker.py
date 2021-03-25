from value_algorithm import rv_dataframe_results
import streamlit as st
import time
import numpy as np
import sys
sys.path.insert(1, '/app/botofwallstreet/')

stock_bought_value = []
total_money_spent_value = 0
num_of_stocks_value = []

for i in range(0, 10):
    stock_bought_value.append(rv_dataframe_results.loc[i, 'Ticker'])
    num_of_stocks_value.append(
        rv_dataframe_results.loc[i, 'Number of Shares Bought'])
    total_money_spent_value += int(rv_dataframe_results.loc[i, 'Total Price'])
