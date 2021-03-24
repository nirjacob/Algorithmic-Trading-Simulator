import streamlit as st
import numpy as np
from sp500EqualWeight import final_dataframe
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
