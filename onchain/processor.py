from __future__ import annotations

from onchain.whale_tracker import WhaleTracker
from onchain.exchange_flow import ExchangeFlow
from onchain.stablecoin import StablecoinTracker
from onchain.smart_money import SmartMoneyTracker
from onchain.feature_builder import OnChainFeatureBuilder


class OnChainProcessor:

    def __init__(self):
        self.whale = WhaleTracker()
        self.flow = ExchangeFlow()
        self.stable = StablecoinTracker()
        self.smart = SmartMoneyTracker()
        self.builder = OnChainFeatureBuilder()

    def process(
        self,
        event,
    ):
        if event is None:
            raise ValueError(
                "OnChainProcessor received no historical event."
            )

        whale = self.whale.detect(event)
        flow = self.flow.classify(event)
        result = self.builder.build(
            event,
            whale,
            flow,
        )

        if result is None:
            raise RuntimeError(
                "OnChainFeatureBuilder returned no historical features."
            )

        return result