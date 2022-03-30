'''
AutoTrader Indiview
--------------------
A general script to view price data and indicators.
'''

from autotrader.autodata import GetData
from autotrader.autoplot import AutoPlot
from autotrader import indicators

# Instantiate GetData class
get_data = GetData()

# Get price data for EUR/USD
instrument = 'EURUSD=X'
data = get_data.yahoo(instrument, '1h', 
                      start_time='2021-01-01', 
                      end_time='2021-03-01')

# Construct indicators dictionary
halftrend_df = indicators.halftrend(data)
indicator_dict = {'HalfTrend': {'type': 'HalfTrend',
                                'data': halftrend_df}}

# Instantiate AutoPlot and plot
ap = AutoPlot(data)
ap.plot(indicators=indicator_dict, instrument=instrument)