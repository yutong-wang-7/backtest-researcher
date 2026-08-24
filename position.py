class Position:
    def __init__(self):
        self.size = 0
        self.average_price = 0.0
        self.realized_pnl = 0.0

    def __repr__(self):
        return (
            f"Position("
            f"size={self.size}, "
            f"average_price={self.average_price:.2f}, "
            f"realized_pnl={self.realized_pnl:.2f}"
            f")"
        )