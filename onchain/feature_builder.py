import numpy as np


class OnChainFeatureBuilder:

    def build(

        self,

        event,

        whale,

        flow

    ):

        return {

            "usd_value":

                event.usd_value,

            "whale":

                float(whale),

            "exchange_flow":

                flow,

            "confidence":

                event.confidence,

            "asset":

                event.asset
        }