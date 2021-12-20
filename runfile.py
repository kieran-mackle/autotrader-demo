'''
AutoTrader Demo Runfile.
------------------------
To run a strategy, simply specify the name of the strategy's configuration
filename prefix in the "add_strategy()" method on line 12.
'''

from autotrader.autotrader import AutoTrader

at = AutoTrader()
at.configure(show_plot=True, verbosity=1)
at.add_strategy('sma_momentum')
at.backtest(start = '10/12/2021',
            end = '19/12/2021',
            initial_balance=1000,
            leverage = 30)
at.optimise(opt_params=['sma_period'],
            bounds=[(20, 60)])
at.run()
