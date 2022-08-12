import numpy as np


class Rebalance:
    '''
    Portfolio rebalancer
    --------------------
    This strategy provides an example of a portfolio rebalancing strategy. It 
    involves rebalancing three ETF's according to a 40/40/20 percentage split:
        VAS: 40%
        VGS: 40% 
        VGB: 20%
    These percentages and ETF's are provided by the 'rebalance_percentages' of
    the configuration file. 
    
    Rebalancing occurs every 7 days, as dictated by the 'rebalance_every_N_days'
    key of the configuration. There is also a 'rebalance_pc_tolerance' parameter,
    which is used to control how many decimals the trade sizes are rounded to.
    
    Note that the 'INCLUDE_BROKER' key is also included in the configuration
    file. This signals to AutoTrader that the strategy requires direct access
    to the broker (and possibly the broker utilities module), and so these 
    must be included in the strategy's __init__ method. Including the 
    broker allows us to access all methods of the broker's module, but 
    specifically, to check the margin available on the account.
    
    '''
    
    def __init__(self, parameters, data, instrument, broker, broker_utils):
        ''' Define all indicators used in the strategy '''
        self.name   = "Portfolio rebalancer"
        self.data   = data
        self.params = parameters
        self.instrument = instrument
        self.broker = broker
        self.last_rebalance = None
        
    def generate_signal(self, i):
        ''' Define strategy to determine entry signals '''
        
        signal_dict = {'order_type': 'market',
                       'direction': 0}
        
        # Get current positions held by account
        rebalance_instruments = list(self.params['rebalance_percentages'].keys())
        current_holdings = self.broker.get_positions()

        if all(inst in current_holdings.keys() for inst in rebalance_instruments):
            # A position is held in all of the rebalance instruments
            
            # Check if it is time to rebalance
            current_time = self.data.index[i]
            days_since_last_rebalance = (current_time - self.last_rebalance).days
            
            # # START PRINTOUT TO MONITOR ASSET ALLOCATION
            # asset_allocation = {}
            # total_value = 0
            # for instrument in rebalance_instruments:
            #     position_value = current_holdings[instrument]['total_margin']
            #     asset_allocation[instrument] = position_value
            #     total_value += position_value
            
            # pc_allocation = {}
            # for instrument in asset_allocation:
            #     pc_allocation[instrument] = round(100*asset_allocation[instrument]/total_value,2)
            
            # print(f"Asset allocation percentages: {pc_allocation}")
            # # END PRINTOUT TO MONITOR ASSET ALLOCATION
            
            if days_since_last_rebalance >= self.params['rebalance_every_N_days']:
                # Calculate current asset allocation
                asset_allocation = {}
                total_value = 0
                for instrument in rebalance_instruments:
                    position_value = current_holdings[instrument].total_margin
                    asset_allocation[instrument] = position_value
                    total_value += position_value
                
                allocation_error = abs(100*asset_allocation[self.instrument]/total_value - \
                    self.params['rebalance_percentages'][self.instrument])
                
                if allocation_error > self.params['rebalance_pc_tolerance']:
                    # Rebalance required
                    # print(" REBALANCING")
                    
                    # Calculate required size to meet balance percentage
                    required_size = self.calculate_position_size(self.data.Close[i])
                    
                    # Calculate difference between required size and current position size
                    size_difference = required_size - current_holdings[self.instrument].long_units
                    
                    # Place order using calculated size difference to rebalance
                    signal_dict['direction'] = np.sign(size_difference)
                    signal_dict['size'] = self.check_margin_requirements(self.data.Close[i], size_difference)
                    
                # Reset last_rebalance time
                self.last_rebalance = current_time
            
        else:
            # Haven't acquired all rebalance instruments yet
            if self.instrument not in current_holdings:
                signal_dict['direction'] = 1 # buy
                nominal_size = self.calculate_position_size(self.data.Close[i])
                signal_dict['size'] = self.check_margin_requirements(self.data.Close[i], nominal_size)
                
                # Assign time to last_rebalance attribute
                self.last_rebalance = self.data.index[i]
        
        return signal_dict
    
    def check_margin_requirements(self, price, size):
        ''' Returns maximum position size that satisfies margin requirements. '''
        
        # Check margin available
        margin_available = self.broker.get_margin_available()
        
        # Check trade will pass margin requirements
        margin_required = price*size / self.params['account_leverage']
        
        while margin_required > margin_available:
            size *= 0.99 # reduce size by 1%
            margin_required = price*size / self.params['account_leverage']
        
        return size
    
    def calculate_position_size(self, price):
        ''' 
        Calculates position size of instrument based on desired position
        value and current price per unit.
        '''
        account_balance = self.broker.get_balance()
        instrument_allocation_pc = self.params['rebalance_percentages'][self.instrument] / 100
        instrument_allocation_value = instrument_allocation_pc * account_balance * self.params['account_leverage']
        position_size = np.floor((instrument_allocation_value / price)* \
                                 10**self.params['partial_trade_rounding'])/10**self.params['partial_trade_rounding']
        return position_size
    