from autotrader import AutoTrader

# Create AutoTrader instance, configure it, and run backtest
at = AutoTrader()
at.configure(verbosity=1, show_plot=True, feed="yahoo")
# at.add_strategy("long_ema_crossover")
# at.add_strategy("ema_crossover")
at.add_strategy("macd")
at.backtest(start="1/6/2023", end="1/2/2024", localize_to_utc=True)
at.virtual_account_config(initial_balance=1000, leverage=30)
at.run()
