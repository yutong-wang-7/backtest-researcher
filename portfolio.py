from position import Position

class Portfolio:
    def __init__(self, initial_cash=100_000):
        self.cash = initial_cash
        self.position = Position()

    def execute_trade(self, side, size, price, commission):

        if side == "BUY":
            self.cash -= price + commission
            self._buy(self.position, size, price)

        elif side == "SELL":
            self.cash += price - commission
            self._sell(self.position, size, price)

        else:
            raise ValueError(f"Invalid side: {side}")

    def _buy(self, position, size, price):
        if position.size >= 0:
            # Increasing a long position
            total_cost = (position.size * position.average_price + size * price)

            position.size += size

            if position.size > 0:
                position.average_price = total_cost / position.size

        else:
            # Closing/reducing a short position
            closing_size = min(size, -position.size)

            position.realized_pnl += (position.average_price - price) * closing_size

            position.size += closing_size

            # If we bought more than needed to close the short,
            # the remainder creates a long position.
            remaining = size - closing_size

            if remaining > 0:
                position.size = remaining
                position.average_price = price

    def _sell(self, position, size, price):
        if position.size <= 0:
            # Increasing a short position
            total_cost = (abs(position.size) * position.average_price + size * price)

            position.size -= size

            if position.size < 0:
                position.average_price = total_cost / abs(position.size)

        else:
            # Closing/reducing a long position
            closing_size = min(size, position.size)

            position.realized_pnl += (price - position.average_price) * closing_size

            position.size -= closing_size

            # If we sold more than needed to close the long,
            # the remainder creates a short position.
            remaining = size - closing_size

            if remaining > 0:
                position.size = -remaining
                position.average_price = price