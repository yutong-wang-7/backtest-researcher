# Backtest Researcher

A modular Python backtesting framework designed to combine the **flexibility of event-driven backtesters** like Backtrader with the **speed and research-oriented workflow** of vectorized frameworks like VectorBT.

> **Status:** Work in progress

## Overview

This project is a from-scratch backtesting engine for developing, testing, and analyzing quantitative trading strategies.

The goal is not simply to build another backtesting library, but to understand how a backtesting framework works internally while creating an architecture that can eventually support both:

* **Flexible strategy simulation** — strategies can make decisions sequentially and interact with portfolio state.
* **Large-scale quantitative research** — strategies can be evaluated efficiently across large datasets and parameter spaces.
* **Realistic execution modeling** — orders, slippage, commissions, positions, and portfolio accounting are handled explicitly.
* **Research tooling** — performance analysis, parameter sweeps, and eventually automated detection of common backtesting biases.

## Architecture

The framework is built around several core components:

```text
Data
 │
 ▼
DataFeed ──────► Strategy
 │                  │
 │                  ▼
 │               Orders
 │                  │
 │                  ▼
 └──────────────► Broker
                    │
                    ▼
                 Position
                    │
                    ▼
                Portfolio
                    │
                    ▼
                 Analyzer
```

### Data

Responsible for providing historical market data to the engine.

The data layer is designed around concepts such as:

* `Data`
* `DataFeed`
* `DataSeries`

The goal is to provide a consistent interface for accessing OHLCV data and other market information while keeping the strategy independent of the underlying data source.

### Strategy

A strategy contains the trading logic.

At each simulation step, the strategy can:

1. Read the current market data.
2. Read indicators and portfolio state.
3. Decide whether to trade.
4. Submit an order to the broker.

The strategy should **not directly modify the portfolio**. Instead, it submits orders and allows the broker/execution system to determine what actually happens.

### Orders

Orders represent the strategy's intent to trade.

For example:

```text
Market Order
Limit Order
Stop Order
Stop-Limit Order
```

An order contains information such as:

* Instrument
* Quantity
* Direction
* Order type
* Limit/stop price where applicable
* Status
* Execution information

Separating orders from execution allows the framework to model the difference between **what the strategy requests** and **what the market actually executes**.

### Broker

The broker is responsible for simulating trading mechanics.

It handles things such as:

* Order submission
* Order execution
* Cash
* Commissions
* Slippage
* Position updates
* Portfolio value
* Margin/leverage where supported

A key design principle is:

> **The strategy decides what it wants to do; the broker decides what actually happens.**

### Position

A position represents the current exposure to an instrument.

A position should contain information such as:

```text
quantity
average entry price
realized P&L
unrealized P&L
```

Both long and short positions should be supported.

### Portfolio

The portfolio represents the overall account.

It tracks:

* Cash
* Positions
* Equity
* Portfolio value
* P&L
* Exposure

The portfolio is distinct from the broker so that account state and execution mechanics remain conceptually separate.

## Execution Model

One of the main goals of this project is to avoid unrealistic backtests.

For example, a strategy observing a bar should not automatically receive the exact price it sees when placing an order if that price would not have been available at the time.

The execution system will eventually account for:

* Market order execution
* Bid/ask spreads
* Slippage
* Commissions
* Order timing
* Partial fills
* Limit-order behavior
* Stop-order behavior

This separation is important for preventing artificially optimistic results.

## Research Workflow

The intended workflow is:

```text
Historical Data
      │
      ▼
Strategy
      │
      ▼
Backtest
      │
      ├──► Trades
      ├──► Portfolio Value
      ├──► Returns
      └──► Statistics
              │
              ▼
        Strategy Analysis
```

For larger research tasks:

```text
Strategy
   │
   ▼
Parameter Grid
   │
   ├── Parameter Set 1 ──► Backtest
   ├── Parameter Set 2 ──► Backtest
   ├── Parameter Set 3 ──► Backtest
   └── ...
            │
            ▼
       Compare Results
```

This parameter-sweep capability is intended to make the framework useful not only for individual backtests but also for systematic strategy research.

## Design Goals

### 1. Flexibility

Strategies should be able to contain arbitrary Python logic rather than being restricted to a small collection of vectorized operations.

### 2. Speed

Large numbers of backtests and parameter combinations should eventually be executable efficiently.

### 3. Realism

The engine should model execution and portfolio accounting closely enough that backtest results are meaningful.

### 4. Modularity

Major components should have well-defined responsibilities so that individual parts can be replaced or extended without rewriting the entire engine.

### 5. Research Safety

The framework will eventually include tools for identifying common sources of misleading backtest results, including:

* Look-ahead bias
* Survivorship bias
* Data leakage
* Overfitting
* Excessive parameter optimization
* Unrealistic transaction costs

## Project Roadmap

### Phase 1 — Core Backtesting Engine

* [ ] Data and data feeds
* [ ] Strategy interface
* [ ] Indicators
* [ ] Orders
* [ ] Broker
* [ ] Position management
* [ ] Portfolio accounting
* [ ] Basic execution model
* [ ] Commission and slippage
* [ ] Trade history

### Phase 2 — Analysis & Research

* [ ] Performance metrics
* [ ] Equity curves
* [ ] Drawdown analysis
* [ ] Sharpe ratio
* [ ] Trade statistics
* [ ] Parameter sweeps
* [ ] Batch backtesting
* [ ] Result storage and comparison

### Phase 3 — Research Integrity

* [ ] Look-ahead bias detection
* [ ] Data leakage detection
* [ ] Survivorship-bias warnings
* [ ] Data/strategy validation
* [ ] Automated backtest diagnostics
* [ ] Research reports

### Phase 4 — Optimization

* [ ] Vectorized execution where possible
* [ ] Parallel backtesting
* [ ] Efficient parameter sweeps
* [ ] Caching
* [ ] Profiling and performance optimization

## Example

A strategy might eventually look like:

```python
class MovingAverageStrategy(Strategy):

    def next(self):
        if self.data.close > self.sma:
            self.buy()

        elif self.data.close < self.sma:
            self.sell()
```

The strategy does not need to know how orders are filled or how portfolio accounting works. Those responsibilities belong to the execution and portfolio layers.

## Why Build This?

Existing frameworks such as Backtrader and VectorBT already provide powerful backtesting capabilities.

This project is primarily an effort to understand and implement the underlying architecture while exploring a combination of two approaches:

**Event-driven flexibility**

* Stateful strategies
* Explicit orders
* Realistic execution
* Complex trading logic

**Vectorized research**

* Fast computation
* Large parameter sweeps
* Efficient batch experiments
* Research-oriented analysis

The long-term objective is to build a framework that makes it easy to move from:

> **"I have a trading idea."**

to

> **"I can systematically test, analyze, and validate that idea."**

## Disclaimer

This project is intended for educational and research purposes. Backtest results are simulations and do not guarantee future trading performance.
