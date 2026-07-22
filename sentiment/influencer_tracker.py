class InfluencerTracker:

    WEIGHTS = {

        "elonmusk": 10,

        "cz_binance": 9.8,

        "vitalikbuterin": 9.5,

        "saylor": 9.2
    }

    def score(

        self,

        username

    ):

        return self.WEIGHTS.get(

            username.lower(),

            1.0

        )