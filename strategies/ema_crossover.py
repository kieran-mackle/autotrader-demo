from finta import TA
from autotrader import Order
from autotrader.indicators import crossover


class EMAcrossOver:
    """EMA Crossover example strategy.

    Entry signals are on crosses of two EMA's, with a stop-loss
    set using the ATR. 
    """
    
    def __init__(self, parameters, data, instrument):
        """Define all indicators used in the strategy."""
        self.name = "EMA Crossover Strategy"
        self.instrument = instrument
        self.data = data
        self.parameters = parameters
        
        # Construct indicators dict for plotting
        self.indicators = {
            'Fast EMA': {
                'type': 'MA',
                'data': TA.EMA(data, self.parameters['fast_ema'])
            },
            'Slow EMA': {
                'type': 'MA',
                'data': TA.EMA(data, self.parameters['slow_ema'])
            }
        }
    
    def generate_features(self, data):
        """Calculates the indicators required to run the strategy."""
        # EMA's
        slow_ema = TA.EMA(data, self.parameters['slow_ema'])
        fast_ema = TA.EMA(data, self.parameters['fast_ema'])
        
        crossovers = crossover(fast_ema, slow_ema)
        
        # ATR for stops
        atr = TA.ATR(data, 14)

        return crossovers, atr

    def generate_signal(self, data):
        """Define strategy to determine entry signals."""
        crossovers, atr = self.generate_features(data)

        RR = self.parameters['RR']
        if crossovers[-1] > 0:
            # Fast EMA has crossed above slow EMA, go long
            stop = data["Close"][-1] - 2*atr[-1]
            take = data["Close"][-1] + RR*(data["Close"][-1] - stop)

            order = Order(
                instrument=self.instrument,
                direction=1,
                stop_loss=stop,
                take_profit=take,
            )
            
        elif crossovers[-1] < 0:
            # Fast EMA has crossed below slow EMA, go short
            stop = data["Close"][-1] + 2*atr[-1]
            take = data["Close"][-1] + RR*(data["Close"][-1] - stop)

            order = Order(
                instrument=self.instrument,
                direction=-1,
                stop_loss=stop,
                take_profit=take,
            )
        
        else:
            # No signal - create blank order
            order = Order()
        
        return order
