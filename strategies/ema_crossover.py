import pandas as pd
from finta import TA
from autotrader import Order
from datetime import datetime
from autotrader.strategy import Strategy
from autotrader.indicators import crossover
from autotrader.brokers.broker import Broker


class EMAcrossOver(Strategy):
    """EMA Crossover example strategy.

    Entry signals are on crosses of two EMA's, with a stop-loss
    set using the ATR.
    """

    def __init__(
        self, parameters: dict, instrument: str, broker: Broker, *args, **kwargs
    ) -> None:
        """Define all indicators used in the strategy."""
        self.name = "EMA Crossover Strategy"
        self.instrument = instrument
        self.parameters = parameters
        self.broker = broker

    def create_plotting_indicators(self, data: pd.DataFrame):
        # Construct indicators dict for plotting
        self.indicators = {
            "Fast EMA": {
                "type": "MA",
                "data": TA.EMA(data, self.parameters["fast_ema"]),
            },
            "Slow EMA": {
                "type": "MA",
                "data": TA.EMA(data, self.parameters["slow_ema"]),
            },
        }

    def generate_features(self, data: pd.DataFrame):
        """Calculates the indicators required to run the strategy."""
        # EMA's
        slow_ema = TA.EMA(data, self.parameters["slow_ema"])
        fast_ema = TA.EMA(data, self.parameters["fast_ema"])

        crossovers = crossover(fast_ema, slow_ema)

        # ATR for stops
        atr = TA.ATR(data, 14)

        return crossovers, atr

    def generate_signal(self, dt: datetime):
        """Define strategy to determine entry signals."""
        # Get OHLCV data
        data = self.broker.get_candles(self.instrument, granularity="1h", count=300)
        if len(data) < 300:
            # This was previously a check in AT
            return None

        # Calculate indicators
        crossovers, atr = self.generate_features(data)

        RR = self.parameters["RR"]
        if crossovers.iloc[-1] > 0:
            # Fast EMA has crossed above slow EMA, go long
            stop = data["Close"].iloc[-1] - 2 * atr.iloc[-1]
            take = data["Close"].iloc[-1] + RR * (data["Close"].iloc[-1] - stop)

            order = Order(
                instrument=self.instrument,
                direction=1,
                size=10,
                stop_loss=stop,
                take_profit=take,
            )

        elif crossovers.iloc[-1] < 0:
            # Fast EMA has crossed below slow EMA, go short
            stop = data["Close"].iloc[-1] + 2 * atr.iloc[-1]
            take = data["Close"].iloc[-1] + RR * (data["Close"].iloc[-1] - stop)

            order = Order(
                instrument=self.instrument,
                direction=-1,
                size=10,
                stop_loss=stop,
                take_profit=take,
            )

        else:
            # No signal
            order = None

        return order
