"""Example script to use AutoTrader for manual trading via API.

It is recommeded that you run this in an interactive environment, such 
as IPython. Otherwise, you must copy and paste these commands in a 
Python terminal, rather than just running the script.

This is a good way to play around and test things before automating them
in a strategy.
"""

from autotrader import AutoTrader, Order


# Instantiate AutoTrader and configure the exchange to trade on/immitate
at = AutoTrader()
at.configure(broker="ccxt:bybit")

# If you want to simulate trading on the exchange (but use real data from it),
# configure a virtual account:
at.virtual_account_config(verbosity=1, exchange="ccxt:bybit", leverage=10)

# Note that if you exclude the line above, you will connect to the real
# exchange specified.

# Run AutoTrader to get the broker connection(s)
broker = at.run()

# If you configured a virtual account above, the broker here will be an instance
# of the Virtual broker. Otherwise, it will be a real exchange connection (eg.
# bybit above), assuming you have provided valid keys.

# Now you can interact with the broker
book = broker.get_orderbook("BTC/USDT:USDT")
print(book.midprice)

# Create an order:
# o = Order("MAGIC/USDT:USDT", direction=1, size=1)
# broker.place_order(o)
