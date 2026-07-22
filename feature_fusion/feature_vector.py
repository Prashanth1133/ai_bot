from dataclasses import dataclass, field


@dataclass(slots=True)
class FeatureVector:

    symbol: str

    timeframe: str

    timestamp: int

    values: dict = field(default_factory=dict)

    def add(

        self,

        key,

        value

    ):

        self.values[key] = value

    def get(self):

        return self.values