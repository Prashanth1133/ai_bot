from ai.signal_engine import (
    SignalEngine
)

from ai.risk_manager import (
    RiskManager
)


class ProductionManager:


    def __init__(self):

        self.risk = RiskManager()


    def decision(

        self,
        prediction

    ):


        signal = (

            SignalEngine.signal(

                prediction

            )

        )


        confidence = prediction.get(

            "confidence",
            0

        )


        take_profit = prediction.get(

            "take_profit",
            0

        )


        stop_loss = prediction.get(

            "stop_loss",
            0

        )


        approved = (

            self.risk.allowed(

                confidence

            )

        )


        action = "NO TRADE"


        if approved:


            if signal == "BUY":

                action = (

                    "EXECUTE BUY"

                )


            elif signal == "SELL":

                action = (

                    "EXECUTE SELL"

                )


        return {

            "signal":

            signal,

            "approved":

            approved,

            "confidence":

            confidence,

            "tp":

            take_profit,

            "sl":

            stop_loss,

            "action":

            action

        }