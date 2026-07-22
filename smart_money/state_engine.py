from collections import defaultdict

from smart_money.market_state import MarketState
from smart_money.market_state import Trend


class StateEngine:

    def __init__(self):

        self.states = defaultdict(MarketState)

    def update(

        self,

        symbol,

        structure

    ):

        state = self.states[symbol]

        state.bos = False
        state.choch = False

        if structure == "HH":

            state.trend = Trend.BULLISH

        elif structure == "HL":

            state.trend = Trend.BULLISH

        elif structure == "LL":

            state.trend = Trend.BEARISH

        elif structure == "LH":

            state.trend = Trend.BEARISH

        return state