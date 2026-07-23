class RiskManager:


    def __init__(

        self,
        risk_percent=1

    ):


        self.risk = risk_percent


    def calculate_position_size(

        self,
        balance,
        stop_loss_percent

    ):


        amount = (

            balance *

            (self.risk/100)

        )


        position_size = (

            amount/

            stop_loss_percent

        )


        return position_size


    def allowed(

        self,
        confidence

    ):


        return confidence >= 0.85