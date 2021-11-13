<p align="center">
  <a href="https://kieran-mackle.github.io/AutoTrader/">
    <img src="https://user-images.githubusercontent.com/60687606/132320916-23445f43-dfdc-4949-9881-e18f622605d2.png" alt="AutoTrader Logo" width="15%" >
  </a>
</p>

<h1 align="center">Welcome to the AutoTrader Demo Repository</h1>

This repository contains example files to help you get started with [AutoTrader](https://github.com/kieran-mackle/AutoTrader). More strategies will be added over time.

## Getting Started
### Install AutoTrader
To run the strategies in this repository, you must first have AutoTrader installed. The easiest way to do so is by using pip:
```
pip install autotrader
```

### Download this Repository
Clone this repository by your preffered method. If you are new to git, simply click the green 'code' button at the top right of this page and download the zip. 
Alternatively, click [here](https://github.com/kieran-mackle/autotrader-demo/archive/refs/heads/main.zip). You can also clone the repository on the command line using:

```
git clone https://github.com/kieran-mackle/autotrader-demo/ 
```

### Backtest a Strategy
After cloning this repo, you are ready to begin backtesting any of the strategies. Simply run `runfile.py`, after specifying the name of the strategy's configuration file (located in the `config/` directory). For example, to run the MACD Crossover Trend Strategy, the runfile will look as so:

```py
from autotrader.autotrader import AutoTrader      # Import AutoTrader

at = AutoTrader()                                 # Create AutoTrader instance
at.configure(show_plot=True, verbosity=1)         # Configure the settings of AutoTrader
at.add_strategy('macd')                           # Provide the name of the strategy configuration file
at.backtest(start = '1/1/2020',                   # Configure the backtest
            end = '1/1/2021',
            initial_balance=1000,
            leverage = 30)
at.run()                                          # Run AutoTrader
```

### Tutorials
If you would like a detailed explanation of how to construct a strategy with AutoTrader, refer to the tutorials on the AutoTrader website, by clicking 
[here](https://kieran-mackle.github.io/AutoTrader/tutorials).

## Demo Strategies
The following is a list of demo strategies provided.

- MACD Crossover Trend Strategy (from the website [tutorials](https://kieran-mackle.github.io/AutoTrader/tutorials/strategy))
- EMA Crossover Strategy (long only example plus long/short Forex example)
- SuperTrend Trend Detector ([AutoScan demo](https://kieran-mackle.github.io/AutoTrader/2021/09/27/developing-scanner.html))
- Multiple timeframe EMA Crossover example
- Portfolio rebalancing example

### Requesting a Strategy
Have a strategy you would like to be automated? Request it [here](https://github.com/kieran-mackle/autotrader-demo/issues/new?assignees=&labels=&template=strategy-request.md&title=%5BSTRATEGY+REQUEST%5D).
