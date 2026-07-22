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

    def process(self, event):

        whale = self.whale.detect(event)

        flow = self.flow.classify(event)

        return self.builder.build(

            event,

            whale,

            flow

        )