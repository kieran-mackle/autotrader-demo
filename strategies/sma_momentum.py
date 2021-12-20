# Import packages
from finta import TA

class SMAMomentum():
    '''
    SMA Momentum Strategy (requested by @rahulmr). 
    
    While SMA 44 is rising (last 3-5 candles) on 5 min 
    timeframe if green candle crosses and closes above the 44SMA, 
    then buy order must be placed above high (with buffer like 0.2)
     of that (crossing) candle and stop loss is loss(with some buffer) 
     of same candle.
     
    Target must be 1:4 and Quantity must be calculated based on risk 
    per trade.
    
    '''
    
    def __init__(self, params, data, instrument):
        ''' Define all indicators used in the strategy '''
        self.name   = "SMA Momentum Strategy"
        self.data   = data
        self.params = params
        
        # SMA
        self.sma = TA.SMA(data, int(params['sma_period']))
        
        # Construct indicators dict for plotting
        self.indicators = {'SMA': {'type': 'MA',
                                   'data': self.sma},
                            }
        
    def generate_signal(self, i, current_positions):
        ''' Define strategy to determine entry signals '''
        signal_dict = {}
        RR = self.params['RR']
        
        if self.data.Close[i] > self.sma[i] and \
            self.data.Open[i] < self.sma[i] and \
            (self.data.Close[i] - self.data.Close.shift(self.params['candle_lookback'])[i]) > 0:
            # Long entry signal
            signal  = 1
            stop    = self.data.Low[i] - self.params['exit_buffer']
            take    = self.data.Close[i] + RR*(self.data.Close[i] - stop)
            
        elif self.data.Close[i] < self.sma[i] and \
            self.data.Open[i] > self.sma[i] and \
            (self.data.Close[i] - self.data.Close.shift(self.params['candle_lookback'])[i]) < 0:
            # Short entry signal
            signal  = -1
            stop    = self.data.High[i] + self.params['exit_buffer']
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
        signal_dict["take_profit"] = take
        
        return signal_dict
