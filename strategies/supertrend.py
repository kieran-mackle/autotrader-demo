# -*- coding: utf-8 -*-

# Package import
from autotrader.indicators import supertrend
from finta import TA


class SuperTrendScan:
    """
    Supertrend Signal Generator
    -----------------------------
    The code below was developed for detecting trends using the SuperTrend
    indicator. You can read more about it at:
        https://kieran-mackle.github.io/AutoTrader/blog

    """

    def __init__(self, parameters, data, instrument):
        """Initialise strategy indicators"""
        self.name = "SuperTrend"
        self.data = data
        self.params = parameters

        self.ema200 = TA.EMA(data, 200)
        self.st_df = supertrend(data, period=12, ATR_multiplier=2)

    def generate_signal(self, i, current_position):
        """Generate long and short signals based on SuperTrend Indicator"""

        order_type = "market"
        signal_dict = {}

        if (
            self.data.Close[i] > self.ema200[i]
            and self.st_df.trend[i] == 1
            and self.st_df.trend[i - 1] == -1
        ):
            # Start of uptrend
            signal = 1

        elif (
            self.data.Close[i] < self.ema200[i]
            and self.st_df.trend[i] == -1
            and self.st_df.trend[i - 1] == 1
        ):
            # Start of downtrend
            signal = -1

        else:
            signal = 0

        # Construct signal dictionary
        signal_dict["order_type"] = order_type
        signal_dict["direction"] = signal

        return signal_dict
