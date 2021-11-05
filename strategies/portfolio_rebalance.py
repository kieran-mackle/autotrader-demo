#!/usr/bin/env python3
# -*- coding: utf-8 -*-
class Rebalance:
    '''
    Portfolio rebalancer.
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
        
        # Get current positions held by account
        rebalance_instruments = list(self.params['rebalance_percentages'].keys())
        current_holdings = self.broker.get_open_positions(rebalance_instruments)
        
        
        # First check if the instrument is being held yet, if not, buy
        # will need to consider the price of all others to calculate the 
        # size
        
        
        # work out percentage of each holding 
        # calculate new amount (ie. how much to sell or buy) of self.instrument
        # Let other bots take care of their own instruments
        
        
        # order_type  = 'market'
        signal_dict = {}
        
        return signal_dict
    
    def calculate_position_size(self):
        ''' 
        Calculates position size of instrument based on desired position
        value and current price per unit.
        '''
    