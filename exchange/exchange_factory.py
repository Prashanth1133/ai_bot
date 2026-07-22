from __future__ import annotations

from exchange.binance_rest import BinanceREST
from exchange.binance_ws import BinanceWS


class ExchangeFactory:

    @staticmethod
    def create_binance(
        api_key: str,
        api_secret: str,
        testnet: bool = False,
    ):

        return {
            "rest": BinanceREST(
                api_key,
                api_secret,
                testnet,
            ),
            "ws": BinanceWS(),
        }