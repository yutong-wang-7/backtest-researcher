from order import Order

class Strategy:
    def __init__(self, broker, data, position):
        self.broker = broker
        self.data = data
        self.position = position

    def buy(self, size):
        order = Order(side = "BUY", size = size)
        self.broker.submit_order(order)

    def sell(self, size):
        order = Order(side = "SELL", size = size)
        self.broker.submit_order(order)

    def next(self):
        pass