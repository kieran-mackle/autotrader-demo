# Import packages
import talib
import numpy as np
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
        
        # EMA's
        self.slow_ema = talib.EMA(self.data.Close.values, 
                                  self.params['slow_ema'])
        
        self.fast_ema = talib.EMA(self.data.Close.values, 
                                  self.params['fast_ema'])
        
        self.crossovers = crossover(self.fast_ema, 
                                    self.slow_ema)
        
        # Construct indicators dict for plotting
        self.indicators = {'Fast EMA': {'type': 'MA',
                                        'data': self.fast_ema},
                            'Slow EMA': {'type': 'MA',
                                        'data': self.slow_ema}
                            }
        
    def generate_signal(self, i, current_positions):
        ''' Define strategy to determine entry signals '''
        order_type      = 'market'
        related_orders  = None
        signal_dict     = {}
        
        # Put entry strategy here
        signal      = 0
        if len(current_positions) == 0:
            # Not currently in any position, okay to enter long
            if self.crossovers[i] == 1:
                # Fast EMA has crossed above slow EMA, enter long
                signal = 1
        else:
            # Already in a position, only look for long exits
            if self.crossovers[i] == -1:
                signal = -1
                related_orders = list(current_positions.keys())[0]
                order_type = 'close'
        
        # Calculate exit targets
        exit_dict = self.generate_exit_levels(signal, i)
        
        # Construct signal dictionary
        signal_dict["order_type"]   = order_type
        signal_dict["direction"]    = signal
        signal_dict["stop_loss"]    = exit_dict["stop_loss"]
        signal_dict["stop_type"]    = exit_dict["stop_type"]
        signal_dict["take_profit"]  = exit_dict["take_profit"]
        signal_dict["related_orders"] = related_orders
        
        return signal_dict


    def generate_exit_levels(self, signal, i):
        ''' Function to determine stop loss and take profit levels '''
    
        # Put exit strategy here
        stop = np.nan
        take = np.nan
        stop_type = 'limit'
        
        exit_dict = {'stop_loss'    : stop, 
                      'stop_type'    : stop_type,
                      'take_profit'  : take}
        
        return exit_dict
