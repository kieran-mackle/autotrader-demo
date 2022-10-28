from datetime import datetime
from autotrader import AutoData, AutoPlot, indicators


# Instantiate GetData class
get_data = AutoData(data_source="yahoo")

# Get price data for EUR/USD
instrument = 'EURUSD=X'
data = get_data.fetch(
    instrument=instrument, 
    granularity='1h', 
    start_time=datetime(2021, 1, 1), 
    end_time=datetime(2021, 3, 1),
)

# Construct indicators dictionary
halftrend_df = indicators.halftrend(data)
indicator_dict = {
    'HalfTrend': {
        'type': 'HalfTrend',
        'data': halftrend_df
    }
}

# Instantiate AutoPlot and plot
ap = AutoPlot(data)
ap.plot(indicators=indicator_dict, instrument=instrument)