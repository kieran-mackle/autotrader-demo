'''
AutoTrader Demo Runfile
-----------------------
To run a strategy, simply specify the name of the strategy's configuration
filename prefix in the "add_strategy()" method on line 12.
'''

from autotrader.autotrader import AutoTrader

# Create AutoTrader instance, configure is, and run backtest
at = AutoTrader()
at.configure(verbosity=1, show_plot=True)
at.add_strategy('ema_crossover')
at.backtest(start = '1/8/2021',
            end = '1/1/2022',
            initial_balance=1000,
            leverage = 30)
at.run()

# Extract trading bot(s)
bot = at.get_bots_deployed()

