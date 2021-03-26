from momentum_algorithm import hqm_dataframe_results
import streamlit as st
import time
import numpy as np

stock_bought = []
total_money_spent = 0
num_of_stocks = []

for i in range(0, 10):
    stock_bought.append(hqm_dataframe_results.loc[i, 'Ticker'])
    num_of_stocks.append(
        hqm_dataframe_results.loc[i, 'Number of Shares Bought'])
    total_money_spent += int(hqm_dataframe_results.loc[i, 'Total Price'])
