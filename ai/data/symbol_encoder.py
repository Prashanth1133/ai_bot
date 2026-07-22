from typing import Dict


class SymbolEncoder:

    def __init__(self):

        self.mapping: Dict[str, int] = {

            "BTCUSDT": 0,

            "ETHUSDT": 1,

            "DOGEUSDT": 2,

        }

    def encode(self, symbol: str) -> int:

        return self.mapping[symbol]

    def decode(self, idx: int):

        for k, v in self.mapping.items():

            if v == idx:

                return k

        raise KeyError(idx)