class OrderTracker:

    def __init__(self):

        self.active = {}

    def register(self, order):

        self.active[order.order_id] = order

    def remove(self, order_id):

        self.active.pop(order_id, None)

    def active_orders(self):

        return list(self.active.values())