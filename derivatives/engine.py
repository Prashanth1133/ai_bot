from __future__ import annotations

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

    @staticmethod
    def _number(
        value,
        default=0.0,
    ):
        if value is None:
            return float(default)
        if isinstance(value, bool):
            return float(value)
        try:
            value = float(value)
            if value != value:
                return float(default)
            if value in (
                float("inf"),
                float("-inf"),
            ):
                return float(default)
            return value
        except Exception:
            return float(default)

    def process(
        self,
        snapshot,
        previous_oi,
    ):
        funding = self.funding.analyze(snapshot.funding_rate)
        oi = self.oi.analyze(
            previous_oi,
            snapshot.open_interest,
        )
        taker = self.taker.imbalance(
            snapshot.taker_buy_volume,
            snapshot.taker_sell_volume,
        )
        liquidations = self.liquidations.detect(
            snapshot.liquidation_buy,
            snapshot.liquidation_sell,
        )

        return {
            "funding": self._number(funding),
            "open_interest": self._number(oi),
            "taker_imbalance": self._number(taker),
            "liquidations": bool(liquidations),
        }