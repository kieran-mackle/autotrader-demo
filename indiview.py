# from autotrader.autoplot import AutoPlot
from autotrader.apcleanup import AutoPlot
from autotrader.lib.autodata import GetData
from autotrader.lib.indicators import crossover, cross_values
import talib

get_data = GetData()

instrument = 'EURUSD=X'

data = get_data.yahoo(instrument, '1h', 
                      start_time='2020-01-01', 
                      end_time='2020-08-01')


ema = talib.EMA(data.Close.values, 200)

MACD, MACDsignal, MACDhist = talib.MACD(data.Close.values, 
                                        12, 26, 9)
MACD_CO        = crossover(MACD, MACDsignal)
MACD_CO_vals   = cross_values(MACD, MACDsignal, MACD_CO)

indicators = {'MACD (12/26/9)': {'type': 'MACD',
                                 'macd': MACD,
                                 'signal': MACDsignal,
                                 'histogram': MACDhist,
                                 'crossvals': MACD_CO_vals},
            'EMA (200)': {'type': 'MA',
                          'data': ema},
            'MACD Crossovers': {'type': 'below',
                                'data': MACD_CO}}

ap = AutoPlot(data)
ap.plot(indicators=indicators, 
        instrument=instrument,
        show_fig=False)

