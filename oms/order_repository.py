class OrderRepository:

    def __init__(self):

        self.orders = {}

    def add(self, order):

        self.orders[order.order_id] = order

    def get(self, order_id):

        return self.orders.get(order_id)

    def update(self, order):

        self.orders[order.order_id] = order

    def all(self):

        return list(self.orders.values())