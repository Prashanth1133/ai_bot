class TradeValidator:

    def validate(

        self,

        signal,

    ):

        if signal.side == "HOLD":

            return False

        if signal.confidence < 0.75:

            return False

        return True