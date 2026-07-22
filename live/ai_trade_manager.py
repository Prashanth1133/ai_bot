from live.position_sizer import (
    PositionSizer
)

from live.trailing_stop import (
    TrailingStop
)

from live.take_profit import (
    TakeProfit
)


class AITradeManager:

    def __init__(

        self,
        balance=10000

    ):

        self.balance = balance

        self.sizer = PositionSizer()

        self.trailing = TrailingStop()

        self.tp = TakeProfit()

    def decide(

        self,
        prediction,
        price

    ):

        signal = prediction[

            "signal"

        ]

        confidence = prediction[

            "confidence"

        ]

        if confidence < 0.70:

            return {

                "action": "SKIP"

            }

        if signal == "BUY":

            stop = (

                price * 0.99

            )

            quantity = (

                self.sizer.calculate(

                    self.balance,
                    price,
                    stop

                )

            )

            target = (

                self.tp.calculate(

                    price,
                    stop

                )

            )

            return {

                "action": "BUY",
                "quantity": quantity,
                "stop": stop,
                "target": target

            }

        if signal == "SELL":

            return {

                "action": "SELL"

            }

        return {

            "action": "HOLD"

        }