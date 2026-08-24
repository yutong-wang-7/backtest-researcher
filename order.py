class Order:
    def __init__(self, side, size, order_type="market"):
        self.side = side
        self.size = size
        self.order_type = order_type

        self.status = "SUBMITTED"
        self.filled_size = 0
        self.fill_price = None
        self.commission = 0