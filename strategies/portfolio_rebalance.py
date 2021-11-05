#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import datetime

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
        self.last_rebalance = None
        
    def generate_signal(self, i, current_position):
        ''' Define strategy to determine entry signals '''
        
        signal_dict = {'order_type': 'market',
                       'direction': 0}
        
        # Get current positions held by account
        rebalance_instruments = list(self.params['rebalance_percentages'].keys())
        current_holdings = self.broker.get_open_positions(rebalance_instruments)

        if all(inst in current_holdings.keys() for inst in rebalance_instruments):
            # A position is held in all of the rebalance instruments
            
            # Check if it is time to rebalance
            current_time = self.data.index[i]
            days_since_last_rebalance = (current_time - self.last_rebalance).days
            
            if days_since_last_rebalance >= self.params['rebalance_every_N_days']:
                # Calculate current asset allocation
                asset_allocation = {}
                total_value = 0
                for instrument in rebalance_instruments:
                    position_value = current_holdings[instrument]['total_margin']
                    asset_allocation[instrument] = position_value
                    total_value += position_value
                
                allocation_error = abs(100*asset_allocation[self.instrument]/total_value - \
                    self.params['rebalance_percentages'][self.instrument])
                
                if allocation_error > self.params['rebalance_pc_tolerance']:
                    # Rebalance required
                    
                    # Calculate required size to meet balance percentage
                    required_size = self.calculate_position_size(self.data.Close[i])
                    
                    # Calculate difference between required size and current position size
                    size_difference = required_size - current_holdings[self.instrument]['long_units']
                    
                    # Place order using calculated size difference to rebalance
                    signal_dict['direction'] = np.sign(size_difference)
                    signal_dict['size'] = size_difference
                    
                    # Reset last_rebalance
                    self.last_rebalance = current_time
            
        else:
            # Haven't acquired all rebalance instruments yet
            if self.instrument not in current_holdings:
                signal_dict['direction'] = 1 # buy
                signal_dict['size'] = self.calculate_position_size(self.data.Close[i])
                
                # Assign time to last_rebalance attribute
                self.last_rebalance = self.data.index[i]
        
        
        return signal_dict
    
    def calculate_position_size(self, price):
        ''' 
        Calculates position size of instrument based on desired position
        value and current price per unit.
        '''
        
        # TODO - need to verify functionality
        
        account_balance = self.broker.get_balance()
        instrument_allocation_pc = self.params['rebalance_percentages'][self.instrument] / 100
        instrument_allocation_value = instrument_allocation_pc * account_balance * self.params['account_leverage']
        position_size = np.floor((instrument_allocation_value / price)* \
                                 10**self.params['partial_trade_rounding'])/10**self.params['partial_trade_rounding']
        
        # position_size = 1
        
        return position_size
    