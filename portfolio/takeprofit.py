class TakeProfit:

    def calculate(

        self,

        entry,

        stop,

        rr=3

    ):

        risk = entry - stop

        return entry + risk * rr