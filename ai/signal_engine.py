class SignalEngine:


    @staticmethod
    def signal(

        prediction

    ):


        confidence = prediction[

            "confidence"

        ]


        if confidence < 0.85:

            return "NO TRADE"


        return prediction[

            "signal"

        ]


    @staticmethod
    def executable(

        prediction

    ):


        return (

            prediction["confidence"]

            >= 0.85

        )