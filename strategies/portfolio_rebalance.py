#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class Rebalance:
    '''
    Portfolio rebalancer.
    '''
    
    def __init__(self, params, data, pair):
        ''' Define all indicators used in the strategy '''
        self.name   = "Simple MACD Trend Strategy"
        self.data   = data
        self.params = params
        
        
    def generate_signal(self, i, current_position):
        ''' Define strategy to determine entry signals '''
        
        # Get current positions held by account
        # work out percentage of each holding 
        # calculate new amount (ie. how much to sell or buy) of self.instrument
        # Let other bots take care of their own instruments
        
        # First check if the instrument is being held yet, if not, buy
        # will need to consider the price of all others to calculate the 
        # size
        
        # order_type  = 'market'
        signal_dict = {}
        
        return signal_dict

    