from autotrader.autotrader import AutoTrader

at = AutoTrader()
at.verbosity = 1
at.add_strategy('long_ema_crossover')
at.backtest(start = '1/1/2020',
            end = '1/1/2021')
# at.optimise(opt_params=['slow_ema', 'fast_ema'],
#             bounds=[(10, 50), (5, 30)])
at.show_plot = True
at.run()

# Demo Strategies:
# long_ema_crossover