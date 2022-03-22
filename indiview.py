'''
AutoTrader Indiview
--------------------
A general script to view price data and indicators.
'''
from finta import TA
from autotrader.autodata import GetData
from autotrader.autoplot import AutoPlot
from autotrader.indicators import crossover, cross_values

# Instantiate GetData class
get_data = GetData()

# Get price data for EUR/USD
instrument = 'EURUSD=X'
data = get_data.yahoo(instrument, '1h', 
                      start_time='2021-01-01', 
                      end_time='2021-04-01')

# Calculate indicators
ema50 = TA.EMA(data, 50)
ema200 = TA.EMA(data, 200)
MACD_df = TA.MACD(data, 12, 26, 9)
MACD_CO = crossover(MACD_df.MACD, MACD_df.SIGNAL)
MACD_CO_vals = cross_values(MACD_df.MACD, MACD_df.SIGNAL, MACD_CO)

# Construct indicators dictionary
indicators = {'MACD (12/26/9)': {'type': 'MACD',
                                  'macd': MACD_df.MACD,
                                  'signal': MACD_df.SIGNAL,
                                  'crossvals': MACD_CO_vals},
            'EMA (50)': {'type': 'MA',
                          'data': ema50},
            'EMA (200)': {'type': 'MA',
                          'data': ema200},
            'MACD Crossovers': {'type': 'below',
                                'data': MACD_CO}}

# Instantiate AutoPlot and plot
ap = AutoPlot(data)
ap.plot(indicators=indicators, instrument=instrument)