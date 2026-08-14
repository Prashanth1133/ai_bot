# decision/trade_validator.py


class TradeValidator:


    def validate(
        self,
        signal
    ):

        if signal is None:
            return False


        side = getattr(
            signal,
            "side",
            None
        )


        if side == "HOLD":
            return False


        if signal.confidence < 0.60:
            return False


        return True