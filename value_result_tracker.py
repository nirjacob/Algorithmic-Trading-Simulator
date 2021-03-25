from value_algorithm import rv_dataframe
import streamlit as st
import time
import numpy as np

stock_bought_value = []
total_money_spent_value = 0
num_of_stocks_value = []

for i in range(0, 9):
    stock_bought_value.append(rv_dataframe.loc[i, 'Ticker'])
    num_of_stocks_value.append(rv_dataframe.loc[i, 'Number of Shares Bought'])
    total_money_spent_value += int(rv_dataframe.loc[i, 'Total Price'])
