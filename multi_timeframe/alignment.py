class AlignmentEngine:

    """
    Calculates agreement between
    multiple timeframes.
    """

    def calculate(self, states):

        bullish = 0
        bearish = 0

        for tf in states.values():

            if tf.trend.name == "BULLISH":

                bullish += 1

            elif tf.trend.name == "BEARISH":

                bearish += 1

        total = bullish + bearish

        if total == 0:

            return {

                "alignment": 0,

                "trend": "NEUTRAL"

            }

        if bullish > bearish:

            return {

                "alignment": bullish / total,

                "trend": "BULLISH"

            }

        return {

            "alignment": bearish / total,

            "trend": "BEARISH"

        }