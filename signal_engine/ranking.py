from __future__ import annotations

from models.signal import Signal


class SignalRanking:

    @staticmethod
    def rank(
        signals: list[Signal],
    ) -> list[Signal]:

        return sorted(

            signals,

            key=lambda x: (

                x.score,

                x.confidence,

            ),

            reverse=True,

        )