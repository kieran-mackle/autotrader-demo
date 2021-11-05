#!/usr/bin/env python3
# -*- coding: utf-8 -*-
class Rebalance:
    '''
    Portfolio rebalancer
    --------------------
    
    Size calculation assumes instrument is traded against home currency.
    
    '''
    
    def __init__(self, params, data, instrument, broker, broker_utils):
        ''' Define all indicators used in the strategy '''
        self.name   = "Portfolio rebalancer"
        self.data   = data
        self.params = params
        self.instrument = instrument
        self.broker = broker
        
    def generate_signal(self, i, current_position):
        ''' Define strategy to determine entry signals '''
        
        signal_dict = {'order_type': 'market'}
        
        # Get current positions held by account
        rebalance_instruments = list(self.params['rebalance_percentages'].keys())
        current_holdings = self.broker.get_open_positions(rebalance_instruments)
        
        if len(current_holdings) == 0:
            # Initialise portfolio
            signal_dict['direction'] = 1 # buy
            signal_dict['size'] = self.calculate_position_size()
        
        else:
            # Portfolio has holdings
            
            # Check if it is time to rebalance yet
            self.params['rebalance_interval']
            
            # work out percentage of each holding 
            # calculate new amount (ie. how much to sell or buy) of self.instrument
            # Let other bots take care of their own instruments
        
        return signal_dict
    
    def calculate_position_size(self):
        ''' 
        Calculates position size of instrument based on desired position
        value and current price per unit.
        '''
        
        account_balance = self.broker.get_balance()
        instrument_allocation_pc = self.params['rebalance_percentages'][self.instrument] / 100
        instrument_allocation_value = instrument_allocation_pc * account_balance
        position_size = instrument_allocation_value / self.data.Close[-1]
        
        return position_size
    