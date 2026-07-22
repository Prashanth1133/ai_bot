class RiskManager:

    def position_size(
        self,
        balance,
        risk=0.02
    ):

        return (
            balance * risk
        )

    def stop_loss(
        self,
        price
    ):

        return (
            price * 0.99
        )

    def take_profit(
        self,
        price
    ):

        return (
            price * 1.02
        )