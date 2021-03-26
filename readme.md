
<a href="https://share.streamlit.io/nirjacob/botofwallstreet/main.py" target='_blank' > <h1> :joystick: Try Here </h1></a>
<br>
## Welcome to my trading algorithm simulator!
### :notebook: Strategies:
- #### :electric_plug: Trading Frequency Strategy
  - Calculate and excute trades every 2 seconds, way too slow for high frequency traders to notice, way to fast for day traders to keep up.
- #### :chart_with_upwards_trend: Momentum Algorithm Strategy
  - Choosing high quality momentum(HQM) stocks by using API calls to get information about stock returns over the past year, six months, three month, and one month back, and evaluating its ranking by calculating the mean of those four and thus giving each stock HQM ranking between 0-100.

- #### :chart_with_upwards_trend: Value Algorithm Strategy
  - Choosing highly real valued (RV) stocks by using API calls to get information about price to earnings/book/sales-ratio in addition to enterprise multiple and enterprise value divided by gross profit, using this information to calculate mean of those and thus giving each stock rv ranking between 0-1.


