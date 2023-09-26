import numpy as np
import pandas as pd
from finta import TA
from autotrader import Order
from autotrader.indicators import (
    supertrend,
    candles_between_crosses,
    rolling_signal_list,
)


class SuperTrendScan:
    """
    Supertrend Signal Generator
    -----------------------------
    The code below was developed for detecting trends using the SuperTrend
    indicator. You can read more about it at:
        https://kieran-mackle.github.io/AutoTrader/2021/09/27/developing-scanner.html

    This is a revised version, which will provide signals for a specified period
    after they are first recieved. This will allow manual running of the script
    to pick up trends a few periods later than initially intended.
    """

    def __init__(self, parameters, data, instrument):
        """Initialise strategy."""
        self.name = "SuperTrend"
        self.data = data
        self.parameters = parameters
        self.instrument = instrument

    def generate_features(self, data: pd.DataFrame):
        """Calculates indicators."""
        ema = TA.EMA(data, self.parameters["ema_period"])
        st_df = supertrend(data, period=12, ATR_multiplier=2)

        signals = pd.Series(dtype=int, index=data.index).fillna(0)
        signals[
            (data["Close"] > ema)
            & (st_df["trend"] == 1)
            & (st_df["trend"].shift() == -1)
        ] = 1
        signals[
            (data["Close"] < ema)
            & (st_df["trend"] == -1)
            & (st_df["trend"].shift() == 1)
        ] = -1

        # Candles since last signal
        candles_since_signal = candles_between_crosses(signals)

        # Rolling signal list
        rolling_signal = rolling_signal_list(signals)

        return candles_since_signal, rolling_signal

    def generate_signal(self, data):
        """Generate long and short signals based on SuperTrend
        Indicator."""
        # Generate latest features
        candles_since_signal, rolling_signal = self.generate_features(data)

        if (
            rolling_signal[-1] == 1
            and candles_since_signal[-1] < self.parameters["candle_tol"]
        ):
            # Start of uptrend
            signal = 1

        elif (
            rolling_signal[-1] == -1
            and candles_since_signal[-1] < self.parameters["candle_tol"]
        ):
            # Start of downtrend
            signal = -1

        else:
            signal = 0

        # Construct order
        if signal != 0:
            # Generate order
            order = Order(
                instrument=self.instrument,
                direction=signal,
                size=1,
            )
        else:
            # Generate blank order
            order = Order()

        return order
