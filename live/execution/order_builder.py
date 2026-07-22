class OrderBuilder:

    def build(self, trade):

        return {

            "symbol": trade.symbol,

            "side": trade.side,

            "type": "MARKET",

            "quantity": float(trade.quantity),

        }