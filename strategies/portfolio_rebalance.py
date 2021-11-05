#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np

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
        
        signal_dict = {'order_type': 'market',
                       'direction': 0}
        
        # Get current positions held by account
        rebalance_instruments = list(self.params['rebalance_percentages'].keys())
        current_holdings = self.broker.get_open_positions(rebalance_instruments)
        
        list(set(rebalance_instruments).intersection(current_holdings))
        
        if all(inst in current_holdings.keys() for inst in rebalance_instruments):
            # A position is held in all of the rebalance instruments
            
            current_time = self.data.index
            
            # Will need to keep track of last rebalance time
            # use timedelta here
            # if current_time - last_rebalance > rebalance interval:
            
            # Calculate current asset allocation
            asset_allocation = {}
            total_value = 0
            for instrument in rebalance_instruments:
                position_value = current_holdings[instrument]['total_margin']
                asset_allocation[instrument] = position_value
                total_value += position_value
            
            allocation_error = abs(100*asset_allocation[self.instrument]/total_value - \
                self.params['rebalance_percentages'][self.instrument])
            
            if allocation_error > self.params['rebalance_tolerance']:
                # Rebalance required
                
                # Calculate required size to meet balance percentage
                required_size = self.calculate_position_size()
                
                # Calculate difference between required size and current position size
                size_difference = required_size - current_holdings[self.instrument]['long_units']
                
                # Place order using calculated size difference to rebalance
                signal_dict['direction'] = np.sign(size_difference)
                signal_dict['size'] = size_difference
            
        else:
            # Haven't acquired all rebalance instruments yet
            if self.instrument not in current_holdings:
                signal_dict['direction'] = 1 # buy
                signal_dict['size'] = self.calculate_position_size()
        
        # if len(current_holdings) == 0:
        #     # Initialise portfolio
        #     signal_dict['direction'] = 1 # buy
        #     signal_dict['size'] = self.calculate_position_size()
        
        # else:
        #     # Portfolio has holdings
            
        #     # Check if it is time to rebalance yet
        #     self.params['rebalance_interval']
            
        #     # work out percentage of each holding 
        #     # calculate new amount (ie. how much to sell or buy) of self.instrument
        #     # Let other bots take care of their own instruments
        
        return signal_dict
    
    def calculate_position_size(self):
        ''' 
        Calculates position size of instrument based on desired position
        value and current price per unit.
        '''
        
        # TODO - need to verify functionality
        
        account_balance = self.broker.get_balance()
        instrument_allocation_pc = self.params['rebalance_percentages'][self.instrument] / 100
        instrument_allocation_value = instrument_allocation_pc * account_balance
        position_size = round(instrument_allocation_value / self.data.Close[-1])
        
        position_size = 1
        
        return position_size
    