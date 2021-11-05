'''
AutoTrader Demo Runfile.
------------------------
To run a strategy, simply specify the name of the strategy's configuration
filename prefix in the "add_strategy()" method on line 12.
'''

from autotrader.autotrader import AutoTrader

at = AutoTrader()
at.configure(show_plot=True)
at.add_strategy('rebalance')
at.backtest(start = '1/1/2020',
            end = '1/8/2020',
            leverage = 30,
            initial_balance=1000)
at.run()
