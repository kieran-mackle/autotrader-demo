# Import packages
from finta import TA
from autotrader.lib.indicators import crossover

class LongEMAcrossOver():
    '''
    EMA Crossover example strategy. 
    
    '''
    
    def __init__(self, params, data, instrument):
        ''' Define all indicators used in the strategy '''
        self.name   = "Strategy name"
        self.data   = data
        self.params = params
        self.instrument = instrument
        
        # EMA's
        self.slow_ema = TA.EMA(data, self.params['slow_ema'])
        
        self.fast_ema = TA.EMA(data, self.params['fast_ema'])
        
        self.crossovers = crossover(self.fast_ema, 
                                    self.slow_ema)
        
        # Construct indicators dict for plotting
        self.indicators = {'Fast EMA': {'type': 'MA',
                                        'data': self.fast_ema},
                            'Slow EMA': {'type': 'MA',
                                        'data': self.slow_ema}
                            }
        
    def generate_signal(self, i, current_position):
        ''' Define strategy to determine entry signals '''
        order_type      = 'market'
        related_orders  = None
        signal_dict     = {}
        
        # Put entry strategy here
        signal      = 0
        if len(current_position) == 0:
            # Not currently in any position, okay to enter long
            if self.crossovers[i] == 1:
                # Fast EMA has crossed above slow EMA, enter long
                signal = 1
        else:
            # Already in a position, only look for long exits
            if self.crossovers[i] == -1:
                signal = -1
                related_orders = current_position[self.instrument]['trade_IDs'][0]
                order_type = 'close'
        
        # Construct signal dictionary
        signal_dict["order_type"]   = order_type
        signal_dict["direction"]    = signal
        signal_dict["related_orders"] = related_orders
        
        return signal_dict

