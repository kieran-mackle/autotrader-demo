'''
AutoScan Demonstration
----------------------
'''

# Import AutoTrader
from autotrader.autotrader import AutoTrader

# Create AutoTrader instance
at = AutoTrader()
at.configure(notify=1)
at.scan('supertrend', scan_index='major')
at.run()