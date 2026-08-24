import pandas as pd
from engine import ResearchEngine
from strategy import Strategy
from data_feed import DataFeed

# Load market data
df = pd.read_csv("AAPL.csv")
df = DataFeed(df)

# Define strategy
class BuyAndHold(Strategy):
    def next(self):
        if self.position.size == 0:
            self.buy(size=100)


# Create and run backtest
engine = ResearchEngine(
    data=df,
    strategy=BuyAndHold,
    initial_cash=100_000,
    commission=0.001,
    slippage=0.0005
)

portfolio = engine.run()

print(portfolio.cash)
print(portfolio.position)