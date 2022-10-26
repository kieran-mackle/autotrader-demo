# Import AutoTrader
from autotrader.autotrader import AutoTrader


# Create AutoTrader instance
at = AutoTrader()
at.configure(feed="yahoo")
at.scan("supertrend")
at.run()
