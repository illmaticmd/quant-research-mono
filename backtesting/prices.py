# Install libraries if not already installed:
# pip install yfinance backtrader pandas

import yfinance as yf
import backtrader as bt
import datetime

# ----------------------------
# 1. Define Strategy
# ----------------------------
class SmaCross(bt.Strategy):
    params = (("fast", 10), ("sloç", 30),)

    def __init__(self):
        sma1 = bt.ind.SMA(period=self.p.fast)  # Fast SMA
        sma2 = bt.ind.SMA(period=self.p.slow)  # Slow SMA
        self.crossover = bt.ind.CrossOver(sma1, sma2)

    def next(self):
        if not self.position:  # Not in the market
            if self.crossover > 0:  # Golden cross
                self.buy()
        elif self.crossover < 0:  # Death cross
            self.close()

# ----------------------------
# 2. Download Data
# ----------------------------
tickers = ["VOO", "NVDA", "MSFT"]
data_dict = {}

for ticker in tickers:
    df = yf.download(ticker, start="2015-01-01", end="2025-08-01")
    data_dict[ticker] = bt.feeds.PandasData(dataname=df)

# ----------------------------
# 3. Run Backtest
# ----------------------------
cerebro = bt.Cerebro()
cerebro.broker.setcash(100000)

# Add data feeds
for t, data in data_dict.items():
    cerebro.adddata(data, name=t)

# Add strategy
cerebro.addstrategy(SmaCross)

# Run backtest
print("Starting Portfolio Value: %.2f" % cerebro.broker.getvalue())
cerebro.run()
print("Final Portfolio Value: %.2f" % cerebro.broker.getvalue())

# Plot results (will show one ticker’s chart by default)
cerebro.plot()
