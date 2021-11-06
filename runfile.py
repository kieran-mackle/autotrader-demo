'''
AutoTrader Demo Runfile.
------------------------
To run a strategy, simply specify the name of the strategy's configuration
filename prefix in the "add_strategy()" method on line 12.
'''

from autotrader.autotrader import AutoTrader

at = AutoTrader()
at.configure(show_plot=True, verbosity=1)
at.add_strategy('macd')
at.backtest(start = '1/1/2020',
            end = '1/10/2021',
            initial_balance=1000,
            leverage = 20)
at.run()