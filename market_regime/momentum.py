class MomentumStrength:

    def calculate(

        self,

        rsi,

        macd

    ):

        score = 0

        if rsi > 70:

            score += 0.5

        elif rsi < 30:

            score -= 0.5

        if macd > 0:

            score += 0.5

        else:

            score -= 0.5

        return score