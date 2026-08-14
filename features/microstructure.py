#=========================================
# features/microstructure.py
#=========================================

from decimal import Decimal
from collections import deque
from dataclasses import dataclass

import statistics
import time


#=========================================
# OUTPUT
#=========================================

@dataclass
class MicroStructureMetrics:

    symbol:str

    bid_pressure:float=0.0

    ask_pressure:float=0.0

    orderbook_imbalance:float=0.0

    aggressive_buyers:float=0.0

    aggressive_sellers:float=0.0

    absorption_score:float=0.0

    liquidity_sweep_score:float=0.0

    spoofing_score:float=0.0

    iceberg_score:float=0.0

    whale_score:float=0.0

    execution_pressure:float=0.0

    micro_trend_score:float=0.0

    market_pressure_score:float=0.0

    large_buy_orders:int=0

    large_sell_orders:int=0

    whale_orders:int=0



#=========================================
# ENGINE
#=========================================

class MicroStructureEngine:


    def __init__(

            self,

            history_size=500,

            whale_multiplier=5,

            spoof_multiplier=10

        ):


        self.metrics={}

        self.trade_history={}

        self.orderbook_history={}

        self.history_size=history_size

        self.whale_multiplier=whale_multiplier

        self.spoof_multiplier=spoof_multiplier



    #=====================================

    def _ensure(self,symbol):


        if symbol not in self.metrics:

            self.metrics[symbol]=(

                MicroStructureMetrics(

                    symbol=symbol

                )

            )


        if symbol not in self.trade_history:

            self.trade_history[symbol]=(

                deque(

                    maxlen=self.history_size

                )

            )


        if symbol not in self.orderbook_history:

            self.orderbook_history[symbol]=(

                deque(

                    maxlen=self.history_size

                )

            )


    #=====================================

    def process_trade(

            self,

            trade

        ):


        symbol=trade.symbol

        quantity=float(trade.quantity)

        side=str(trade.side)


        self._ensure(symbol)


        self.trade_history[symbol].append(

            quantity

        )


        average_size=max(

            statistics.mean(

                self.trade_history[symbol]

            ),

            1e-8

        )


        metrics=self.metrics[symbol]


        #---------------------------------
        # LARGE ORDERS
        #---------------------------------

        if quantity > (average_size*3):


            if "BUY" in side:

                metrics.large_buy_orders+=1

            else:

                metrics.large_sell_orders+=1


        #---------------------------------
        # WHALE DETECTION
        #---------------------------------

        if quantity > (

            average_size *

            self.whale_multiplier

        ):

            metrics.whale_orders+=1


        #---------------------------------
        # AGGRESSIVE BUYERS
        #---------------------------------

        if "BUY" in side:

            metrics.aggressive_buyers+=quantity

        else:

            metrics.aggressive_sellers+=quantity


        self.calculate_market_pressure(

            symbol

        )



    #=====================================

    def process_orderbook(

            self,

            orderbook

        ):


        symbol=orderbook.symbol

        self._ensure(symbol)


        metrics=self.metrics[symbol]


        bid_volume=0.0
        ask_volume=0.0


        for level in orderbook.bids:

            bid_volume+=float(level.quantity)


        for level in orderbook.asks:

            ask_volume+=float(level.quantity)



        total=max(

            bid_volume+

            ask_volume,

            1e-8

        )


        metrics.bid_pressure=(

            bid_volume/

            total

        )


        metrics.ask_pressure=(

            ask_volume/

            total

        )


        metrics.orderbook_imbalance=(

            (

                bid_volume-

                ask_volume

            )/

            total

        )


        #--------------------------------
        # absorption
        #--------------------------------

        metrics.absorption_score=(

            abs(

                metrics.orderbook_imbalance

            )

        )


        #--------------------------------
        # spoofing
        #--------------------------------

        if (

            max(

                bid_volume,

                ask_volume

            )

            >

            min(

                bid_volume,

                ask_volume

            )*

            self.spoof_multiplier

        ):

            metrics.spoofing_score=1.0

        else:

            metrics.spoofing_score=0.0


        self.calculate_market_pressure(

            symbol

        )


    #=====================================

    def calculate_market_pressure(

            self,

            symbol

        ):



        metrics=self.metrics[symbol]


        score=0


        score+=(

            metrics.bid_pressure*20

        )


        score+=(

            metrics.orderbook_imbalance*20

        )


        score+=(

            metrics.aggressive_buyers/

            max(

                metrics.aggressive_buyers+

                metrics.aggressive_sellers,

                1

            )

        )*20


        score+=(

            min(

                metrics.whale_orders,

                5

            )*5

        )


        score+=(

            metrics.absorption_score*20

        )


        score+=(

            (

                1-

                metrics.spoofing_score

            )*15

        )


        metrics.market_pressure_score=round(

            score,

            2

        )


    #=====================================

    def get(

            self,

            symbol

        ):


        if symbol not in self.metrics:

            return None


        return self.metrics[symbol]


#=========================================