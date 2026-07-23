class SocialEngine:


    def __init__(self):

        self.score = 50


    def evaluate(

        self,
        mentions,
        engagement

    ):


        score = (

            (mentions*0.40)

            +

            (engagement*0.60)

        )


        if score > 100:

            score = 100


        self.score = round(

            score,

            2

        )


        return {

            "score":

            self.score

        }