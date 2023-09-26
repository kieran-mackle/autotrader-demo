# Import packages
from finta import TA
from autotrader import Order
from autotrader.indicators import crossover


class LongEMAcrossOver:
    """EMA Crossover example strategy."""

    def __init__(self, parameters, data, instrument, broker, **kwargs):
        """Define all indicators used in the strategy."""
        self.name = "Strategy name"
        self.data = data
        self.params = parameters
        self.instrument = instrument
        self.broker = broker

        # EMA's
        self.slow_ema = TA.EMA(data, self.params["slow_ema"])

        self.fast_ema = TA.EMA(data, self.params["fast_ema"])

        self.crossovers = crossover(self.fast_ema, self.slow_ema)

        # Construct indicators dict for plotting
        self.indicators = {
            "Fast EMA": {"type": "MA", "data": self.fast_ema},
            "Slow EMA": {"type": "MA", "data": self.slow_ema},
        }

    def generate_signal(self, i):
        """Define strategy to determine entry signals."""
        orders = []

        # Get current position
        current_position = self.broker.get_positions(self.instrument)

        # Put entry strategy here
        signal = 0
        if len(current_position) == 0:
            # Not currently in any position, okay to enter long
            if self.crossovers[i] == 1:
                # Fast EMA has crossed above slow EMA, enter long
                order = Order(direction=1)
                orders.append(order)
        else:
            # Already in a position, only look for long exits
            if self.crossovers[i] == -1:
                net_position = current_position[self.instrument].net_position
                order = Order(direction=-1, size=-net_position)
                orders.append(order)

        return orders
