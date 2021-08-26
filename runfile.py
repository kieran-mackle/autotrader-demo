from autotrader.autotrader import AutoTrader

at = AutoTrader()
at.verbosity = 1
at.add_strategy('macd')
at.backtest(start = '1/1/2020',
            end = '1/1/2021',
            leverage = 30)
# at.optimise(opt_params=['MACD_fast', 'MACD_slow'],
#             bounds=[(5, 20), (20, 40)])
at.show_plot = True
at.run()


# Demo Strategies:
# long_ema_crossover
# macd (make sure to set leverage appropriately)