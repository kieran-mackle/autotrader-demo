'''
AutoTrader Demo Runfile.
'''

from autotrader.autotrader import AutoTrader

at = AutoTrader()
at.verbosity = 1
at.add_strategy('MTF_ema_crossover')
at.backtest(start = '1/1/2020',
            end = '1/8/2020',
            leverage = 30)
at.show_plot = True
at.run()
