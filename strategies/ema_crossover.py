# Import packages
from finta import TA
from autotrader.indicators import crossover

class EMAcrossOver:
    """EMA Crossover example strategy. 
    """
    
    def __init__(self, params, data, instrument):
        ''' Define all indicators used in the strategy '''
        self.name   = "EMA Crossover Strategy"
        self.data   = data
        self.params = params
        
        # EMA's
        self.slow_ema = TA.EMA(self.data, self.params['slow_ema'])
        
        self.fast_ema = TA.EMA(self.data, self.params['fast_ema'])
        
        self.crossovers = crossover(self.fast_ema, self.slow_ema)
        
        # ATR for stops
        self.atr = TA.ATR(data, 14)
        
        # Construct indicators dict for plotting
        self.indicators = {'Fast EMA': {'type': 'MA',
                                        'data': self.fast_ema},
                            'Slow EMA': {'type': 'MA',
                                        'data': self.slow_ema}
                            }
        
    def generate_signal(self, i, current_positions):
        ''' Define strategy to determine entry signals '''
        signal_dict     = {}
        RR = self.params['RR']
        
        if self.crossovers[i] == 1:
            # Fast EMA has crossed above slow EMA, go long
            signal  = 1
            stop    = self.data.Close[i] - 2*self.atr[i]
            take    = self.data.Close[i] + RR*(self.data.Close[i] - stop)
            
        elif self.crossovers[i] == -1:
            # Fast EMA has crossed below slow EMA, go short
            signal  = -1
            stop    = self.data.Close[i] + 2*self.atr[i]
            take    = self.data.Close[i] + RR*(self.data.Close[i] - stop)
        
        else:
            # No signal
            signal  = 0
            stop    = None
            take    = None
        
        # Construct signal dictionary
        signal_dict["order_type"] = 'market'
        signal_dict["direction"] = signal
        signal_dict["stop_loss"] = stop
        signal_dict["stop_type"] = 'limit'
        signal_dict["take_profit"] = take
        
        return signal_dict
