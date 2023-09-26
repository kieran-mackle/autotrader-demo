from autotrader import AutoTrader

# Create AutoTrader instance, configure it, and run backtest
at = AutoTrader()
at.configure(verbosity=1, show_plot=True, feed="yahoo")
at.add_strategy("ema_crossover")
at.backtest(start="1/1/2021", end="1/5/2022")
at.virtual_account_config(initial_balance=1000, leverage=30)
at.run()
