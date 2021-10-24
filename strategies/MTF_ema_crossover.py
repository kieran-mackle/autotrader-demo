# Import packages
from finta import TA
from autotrader.lib.indicators import crossover

class EMAcrossOver():
    '''
    EMA Crossover example strategy. 
    
    '''
    
    def __init__(self, params, data, instrument):
        ''' Define all indicators used in the strategy '''
        self.name   = "EMA Crossover Strategy"
        self.params = params
        
        # Extract timeframes from data
        # Note that daily_data timezone must be localised to tz of hourly
        # data since it will otherwise be naive
        hourly_data = data['1h']
        daily_data = data['1d'].tz_localize(hourly_data.index.dtype.tz)
        
        # Assign hourly data to class attribute
        self.hourly_data = hourly_data
        
        # Re-index daily data to match dimension of hourly data
        daily_data = daily_data.reindex(hourly_data.index, method='ffill')
        
        # Daily EMA
        self.daily_ema = TA.EMA(daily_data, self.params['daily_ema'])
        
        # Hourly EMA's
        self.slow_ema = TA.EMA(hourly_data, 
                               self.params['slow_ema'])
        
        self.fast_ema = TA.EMA(hourly_data, 
                               self.params['fast_ema'])
        
        self.crossovers = crossover(self.fast_ema, 
                                    self.slow_ema)
        
        # ATR for stops
        self.atr = TA.ATR(hourly_data, 14)
        
        # Construct indicators dict for plotting
        self.indicators = {'Fast EMA': {'type': 'MA',
                                        'data': self.fast_ema},
                           'Slow EMA': {'type': 'MA',
                                        'data': self.slow_ema},
                           'Daily EMA': {'type': 'MA',
                                         'data': self.daily_ema}
                           }
        
    def generate_signal(self, i, current_positions):
        ''' Define strategy to determine entry signals '''
        signal_dict     = {}
        RR = self.params['RR']
        
        if self.crossovers[i] == 1 and self.hourly_data.Close[i] > self.daily_ema[i]:
            # Fast EMA has crossed above slow EMA, go long
            signal  = 1
            stop    = self.hourly_data.Close[i] - 2*self.atr[i]
            take    = self.hourly_data.Close[i] + RR*(self.hourly_data.Close[i] - stop)
            
        elif self.crossovers[i] == -1 and self.hourly_data.Close[i] < self.daily_ema[i]:
            # Fast EMA has crossed below slow EMA, go short
            signal  = -1
            stop    = self.hourly_data.Close[i] + 2*self.atr[i]
            take    = self.hourly_data.Close[i] + RR*(self.hourly_data.Close[i] - stop)
        
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
