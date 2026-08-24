from broker import Broker
from portfolio import Portfolio
from strategy import Strategy

class ResearchEngine:
    """
    Central orchestrator for the quantitative research and backtesting pipeline.

    The ResearchEngine coordinates all major components of a backtest,
    including market data, trading strategies, order execution, portfolio
    accounting, and performance analysis. It does not implement trading
    logic itself; instead, it manages the flow of information between the
    different subsystems.

    A typical backtest proceeds as follows:

        1. Initialize all registered components.
        2. Iterate through historical market data one event (bar/tick) at a time.
        3. Update indicators and market state.
        4. Invoke the strategy to generate trading decisions.
        5. Submit generated orders to the broker.
        6. Simulate order execution.
        7. Update portfolio holdings and account value.
        8. Record statistics and analytics.
        9. Produce final performance reports.

    The engine owns the simulation loop but delegates all domain-specific
    responsibilities to specialized components:

        - DataFeed: Supplies market data.
        - Strategy: Generates trading decisions.
        - Broker: Simulates order execution.
        - Portfolio: Tracks positions, cash, and PnL.
        - Analyzer(s): Compute performance metrics and diagnostics.

    The long-term architecture is intended to be extensible. Additional
    modules, such as parameter optimization, bias detection, experiment
    tracking, or visualization, should be attachable without modifying
    the core simulation loop.

    Notes
    -----
    The ResearchEngine should remain a lightweight coordinator. Business
    logic should reside within the individual components rather than in
    the engine itself. This separation keeps the system modular, testable,
    and easy to extend.
    """
    def __init__(self, data=None, strategy=None, initial_cash = 100_000, commission=0.001, slippage=0.0005):
        self.data = data
        self.portfolio = Portfolio(initial_cash = initial_cash)
        self.broker = Broker(portfolio = self.portfolio, commission = commission, slippage = slippage)
        self.strategy = strategy(data=self.data, broker=self.broker, position = self.portfolio.position)

    def run(self):

        while not self.data.is_finished():
            self.data.next()
            self.strategy.next()
            self.broker.process_orders(self.data)

        return self.portfolio