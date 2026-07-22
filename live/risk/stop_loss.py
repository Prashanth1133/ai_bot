from __future__ import annotations

from decimal import Decimal
from enum import Enum


class StopType(Enum):

    ATR = "atr"

    SWING = "swing"

    ORDER_BLOCK = "order_block"

    LIQUIDITY = "liquidity"


class StopLossCalculator:

    def __init__(

        self,

        atr_multiplier: Decimal,

    ):

        self.multiplier = atr_multiplier

    def atr_stop(

        self,

        entry: Decimal,

        atr: Decimal,

        long: bool,

    ) -> Decimal:

        distance = atr * self.multiplier

        if long:

            return entry - distance

        return entry + distance

    def swing_stop(

        self,

        swing_price: Decimal,

        buffer: Decimal,

        long: bool,

    ) -> Decimal:

        if long:

            return swing_price - buffer

        return swing_price + buffer

    def order_block_stop(

        self,

        block_price: Decimal,

        buffer: Decimal,

        long: bool,

    ) -> Decimal:

        if long:

            return block_price - buffer

        return block_price + buffer