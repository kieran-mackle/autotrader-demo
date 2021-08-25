from autotrader.autotrader import AutoTrader

at = AutoTrader()
at.verbosity = 1
at.add_strategy('long_ema_crossover')
at.backtest(start = '1/1/2020',
            end = '1/3/2020')
at.show_plot = True
at.run()