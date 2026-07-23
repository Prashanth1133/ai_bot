class OptionsEngine:


    def evaluate(

        self,
        put_volume,
        call_volume

    ):


        if call_volume == 0:

            ratio = 0


        else:

            ratio = (

                put_volume/

                call_volume

            )


        if ratio < 0.80:

            signal = "BULLISH"


        elif ratio > 1.20:

            signal = "BEARISH"


        else:

            signal = "NEUTRAL"


        return {

            "signal":

            signal,

            "ratio":

            round(

                ratio,

                4

            )

        }