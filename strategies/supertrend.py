import pandas as pd
from finta import TA
from autotrader import Order
from datetime import datetime
from autotrader.strategy import Strategy
from autotrader.indicators import supertrend
from autotrader.brokers.broker import Broker


class SuperTrendScan(Strategy):
    """
    Supertrend Signal Generator
    -----------------------------
    The code below was developed for detecting trends using the SuperTrend
    indicator. You can read more about it at:
        https://kieran-mackle.github.io/AutoTrader/blog
    """

    def __init__(
        self, parameters: dict, instrument: str, broker: Broker, *args, **kwargs
    ):
        """Initialise strategy indicators"""
        self.name = "SuperTrend"
        self.params = parameters
        self.broker = broker
        self.instrument = instrument

    def caculate_indicators(self, data: pd.DataFrame):
        ema200 = TA.EMA(data, 200)
        st_df = supertrend(data, period=12, ATR_multiplier=2)

        # ATR for stops
        atr = TA.ATR(data, 14)

        return ema200, st_df, atr

    def generate_signal(self, dt: datetime):
        """Generate long and short signals based on SuperTrend Indicator"""
        orders = []

        # Get data and generate indicators
        data = self.broker.get_candles(self.instrument, granularity="1h", count=300)
        if len(data) < 200:
            # Not ready to trade yet
            return None
        ema200, st_df, atr = self.caculate_indicators(data)

        # Create orders
        RR = self.params["RR"]
        if (
            data["Close"].iloc[-1] > ema200.iloc[-1]
            and st_df["trend"].iloc[-1] == 1
            and st_df["trend"].iloc[-2] == -1
        ):
            # Start of uptrend; buy
            stop = data["Close"].iloc[-1] - 2 * atr.iloc[-1]
            take = data["Close"].iloc[-1] + RR * (data["Close"].iloc[-1] - stop)
            order = Order(
                instrument=self.instrument,
                direction=1,
                size=10,
                stop_loss=stop,
                take_profit=take,
            )
            orders.append(order)

        elif (
            data["Close"].iloc[-1] < ema200.iloc[-1]
            and st_df["trend"].iloc[-1] == -1
            and st_df["trend"].iloc[-2] == 1
        ):
            # Start of downtrend; sell
            stop = data["Close"].iloc[-1] + 2 * atr.iloc[-1]
            take = data["Close"].iloc[-1] + RR * (data["Close"].iloc[-1] - stop)
            order = Order(
                instrument=self.instrument,
                direction=-1,
                size=10,
                stop_loss=stop,
                take_profit=take,
            )
            orders.append(order)

        return orders
