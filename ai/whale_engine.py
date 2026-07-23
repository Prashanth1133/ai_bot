class WhaleEngine:


    def __init__(self):

        pass


    def evaluate(

        self,
        buy_volume,
        sell_volume

    ):


        if buy_volume == 0:

            ratio = 0


        else:

            ratio = (

                buy_volume/

                (

                    buy_volume+

                    sell_volume

                )

            )


        if ratio > 0.70:

            label = "BULLISH"


        elif ratio < 0.40:

            label = "BEARISH"


        else:

            label = "NEUTRAL"


        return {

            "ratio":round(

                ratio,

                4

            ),

            "label":

            label

        }