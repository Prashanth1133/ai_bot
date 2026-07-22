class RiskManager:

    def approve(

        self,

        signal,

        confidence,

        drawdown

    ):

        if confidence < 0.75:

            return False

        if drawdown > 0.10:

            return False

        return True