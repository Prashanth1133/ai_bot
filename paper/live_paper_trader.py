import time

from ai.production_manager import (
    ProductionManager
)

from paper.paper_engine import (
    PaperEngine
)


class LivePaperTrader:


    def __init__(

        self,
        inference_engine

    ):

        self.inference = (

            inference_engine

        )

        self.manager = (

            ProductionManager()

        )

        self.paper = (

            PaperEngine()

        )


    def process(

        self,
        trade,
        features,
        risk

    ):


        prediction = (

            self.inference.predict(

                features

            )

        )


        decision = (

            self.manager.decision(

                prediction

            )

        )


        if not decision[

            "approved"

        ]:

            return None


        fill = (

            self.paper.execute(

                trade,
                risk

            )

        )


        return fill


    def stream(

        self,
        generator

    ):


        for trade in generator:


            result = self.process(

                trade.trade,
                trade.features,
                trade.risk

            )


            if result:


                print(

                    "\nExecuted :",

                    result.symbol,

                    result.side,

                    result.price

                )


            time.sleep(

                0.10

            )