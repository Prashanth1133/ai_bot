class PositionSizer:

    def size(

        self,

        account,

        risk_percent,

        stop_distance

    ):

        risk = account * risk_percent

        return risk / stop_distance