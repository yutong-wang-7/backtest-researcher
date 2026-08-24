class Broker:
    def __init__(self, portfolio, commission=0.001, slippage=0.0005):
        self.commission = commission
        self.slippage = slippage
        self.portfolio = portfolio
        self.orders = []

    def submit_order(self, order):
        self.orders.append(order)

    def process_orders(self, data):
        for order in self.orders:
            if self.can_execute(order, data):
                self.execute(order, data)

    def can_execute(self, order, data):
        if order.order_type == "MARKET":
            return True
        return False 

    def execute(self, order, data):
        price = data.close[0]

        # slippage
        if order.side == "BUY":
            execution_price = price * (1 + self.slippage)
        else:
            execution_price = price * (1 - self.slippage)

        # commission
        trade_value = execution_price * order.size
        commission = trade_value * self.commission

        self.portfolio.execute_trade(
            side=order.side,
            size=order.size,
            price=execution_price,
            commission=commission
        )
 
        order.status = "FILLED"
        order.filled_size = order.size
        order.fill_price = execution_price