from derivatives.funding import FundingAnalyzer
from derivatives.open_interest import OpenInterestAnalyzer
from derivatives.taker_volume import TakerVolumeAnalyzer
from derivatives.liquidations import LiquidationAnalyzer


class DerivativesEngine:

    def __init__(self):

        self.funding = FundingAnalyzer()

        self.oi = OpenInterestAnalyzer()

        self.taker = TakerVolumeAnalyzer()

        self.liquidations = LiquidationAnalyzer()

    def process(

        self,

        snapshot,

        previous_oi

    ):

        return {

            "funding":

                self.funding.analyze(

                    snapshot.funding_rate

                ),

            "open_interest":

                self.oi.analyze(

                    previous_oi,

                    snapshot.open_interest

                ),

            "taker_imbalance":

                self.taker.imbalance(

                    snapshot.taker_buy_volume,

                    snapshot.taker_sell_volume

                ),

            "liquidations":

                self.liquidations.detect(

                    snapshot.liquidation_buy,

                    snapshot.liquidation_sell

                )

        }