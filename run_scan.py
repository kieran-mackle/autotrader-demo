'''
AutoScan Demonstration
----------------------
'''

# Import AutoTrader
from autotrader.autotrader import AutoTrader

# Create AutoTrader instance
at = AutoTrader()
at.configure(show_plot=True)
at.add_strategy('ema_crossover')
at.backtest(start = "1/1/2020",
            end = "1/3/2020",
            leverage=1)
at.run()