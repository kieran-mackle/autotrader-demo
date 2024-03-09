# """This is an example of using AutoTraders plotting module."""
from datetime import datetime
from autotrader import AutoTrader, AutoPlot, indicators


# Instantiate AutoTrader and configure the exchange to trade on/immitate
at = AutoTrader()
at.configure(broker="ccxt:bybit")

# Run AutoTrader to get the broker connection(s)
broker = at.run()

# Get candles
instrument = "ETH/USDT"
data = broker.get_candles(
    instrument=instrument,
    granularity="1d",
    start_time=datetime(2023, 1, 1),
    end_time=datetime(2024, 2, 1),
)

# Construct indicators dictionary
halftrend_df = indicators.halftrend(data)
indicator_dict = {"HalfTrend": {"type": "HalfTrend", "data": halftrend_df}}

# Instantiate AutoPlot and plot
ap = AutoPlot(data)
ap.plot(indicators=indicator_dict, instrument=instrument)
