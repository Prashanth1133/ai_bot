from __future__ import annotations

import numpy as np


class OrderBookImbalance:
    """
    Order Book Imbalance

    (Bid - Ask) / (Bid + Ask)
    """

    @staticmethod
    def calculate(

        bid_volume,

        ask_volume,

    ):

        bid = np.asarray(
            bid_volume,
            dtype=float,
        )

        ask = np.asarray(
            ask_volume,
            dtype=float,
        )

        denominator = bid + ask

        return np.divide(

            bid - ask,

            denominator,

            out=np.zeros_like(
                denominator,
            ),

            where=denominator != 0,

        )

    @staticmethod
    def latest(

        bid_volume,

        ask_volume,

    ):

        return OrderBookImbalance.calculate(

            bid_volume,

            ask_volume,

        )[-1]