class StrategyFilter:

    def __init__(

        self,

        minimum_confidence=0.6,

    ):

        self.minimum_confidence = minimum_confidence

    def filter(

        self,

        signals,

    ):

        return [

            signal

            for signal in signals

            if signal.confidence >= self.minimum_confidence

        ]