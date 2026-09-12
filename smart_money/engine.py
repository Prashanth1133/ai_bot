from __future__ import annotations

from indicators.atr import ATRCalculator
from smart_money.adaptive_swing import AdaptiveSwingDetector
from smart_money.market_structure import MarketStructure
from smart_money.break_of_structure import BreakOfStructure
from smart_money.choch import ChangeOfCharacter
from smart_money.state_engine import StateEngine
from smart_money.order_block import OrderBlockDetector
from smart_money.order_block_manager import OrderBlockManager
from smart_money.liquidity import LiquidityDetector
from smart_money.liquidity_manager import LiquidityManager
from smart_money.fair_value_gap import FairValueGapDetector
from smart_money.fvg_manager import FVGManager


class SmartMoneyEngine:

    # Enough history for SMC calculations while preventing
    # O(N²) historical rescanning during dataset generation.
    MAX_HISTORY = 500

    def __init__(self):

        self.swing_detector = AdaptiveSwingDetector()
        self.structure_engine = MarketStructure()
        self.bos_engine = BreakOfStructure()
        self.choch_engine = ChangeOfCharacter()

        self.state_engine = StateEngine()

        self.order_block_detector = OrderBlockDetector()
        self.order_block_manager = OrderBlockManager()

        self.liquidity_detector = LiquidityDetector()
        self.liquidity_manager = LiquidityManager()

        self.fvg_detector = FairValueGapDetector()
        self.fvg_manager = FVGManager(
            max_gaps_per_symbol=500
        )

        self.atr_calculator = ATRCalculator(period=14)
        self._last_processed_time = None
        self._atr_cache = {}
        self._last_result = {}

    def reset(self):

        self.choch_engine.reset()
        self.bos_engine.reset()
        self.swing_detector.reset()

        self.fvg_manager.reset()

        if hasattr(self.order_block_manager, "reset"):
            self.order_block_manager.reset()

        if hasattr(self.liquidity_manager, "reset"):
            self.liquidity_manager.reset()

        if hasattr(self.state_engine, "reset"):
            self.state_engine.reset()

        self.atr_calculator = ATRCalculator(period=14)
        self._last_processed_time = None
        self._atr_cache.clear()
        self._last_result.clear()

    @staticmethod
    def _time(candle):
        return int(
            getattr(candle, "open_time", 0)
        )

    def _calculate_atr(self, candles):
        if not candles:
            return None

        latest = candles[-1]
        atr = self.atr_calculator.update(latest)
        if atr is not None and float(atr) > 0:
            return float(atr)

        # Warmup if needed
        for candle in candles:
            value = self.atr_calculator.update(candle)
            if value is not None:
                atr = value

        if atr is None or float(atr) <= 0:
            return None

        return float(atr)

    def process(self, candles):

        if not candles or len(candles) < 20:
            return None

        candles = sorted(
            candles,
            key=lambda c: self._time(c),
        )

        latest = candles[-1]

        latest_open_time = getattr(latest, "open_time", None)

        if (
            latest_open_time is not None
            and latest_open_time == self._last_processed_time
        ):
            return None

        self._last_processed_time = latest_open_time

        symbol = str(
            latest.symbol
        ).upper()

        # Critical performance protection.
        #
        # Never feed the entire dataset history into SMC.
        history = candles[
            -self.MAX_HISTORY:
        ]

        atr = self._calculate_atr(
            history
        )

        if atr is None:
            return None

        self._atr_cache[symbol] = atr

        swings = self.swing_detector.detect(
            history,
            atr,
        )

        if len(swings) < 2:
            return None

        structure = self.structure_engine.analyze(
            swings
        )

        bos = self.bos_engine.detect(
            candles=history,
            swings=swings,
            structure=structure,
        )

        choch = self.choch_engine.detect(
            structure
        )

        state = self.state_engine.update(
            symbol,
            structure.name,
        )

        blocks = self.order_block_detector.detect(
            history,
            atr,
        )

        for block in blocks:
            self.order_block_manager.add(block)

        # ---------------------------------------------------------
        # FVG: incremental detection only
        # ---------------------------------------------------------
        if len(candles) >= 3:
            recent_fvg_candles = candles[-3:]

            detected_fvgs = self.fvg_detector.detect(
                recent_fvg_candles
            )

            for gap in detected_fvgs:
                self.fvg_manager.add(gap)

        zones = self.liquidity_detector.detect(
            history
        )

        for zone in zones:
            self.liquidity_manager.add(zone)

        latest_close = latest.close

        self.order_block_manager.update(
            symbol,
            latest_close,
        )

        self.liquidity_manager.update(
            symbol,
            latest_close,
        )

        self.fvg_manager.update(
            symbol=symbol,
            price=latest_close,
            current_time=getattr(
                latest,
                "open_time",
                None,
            ),
        )

        result = {
            "symbol": symbol,
            "atr": float(atr),
            "swings": swings,
            "structure": structure,
            "bos": bos,
            "choch": choch,
            "state": state,
            "order_blocks": self.order_block_manager.active(
                symbol
            ),
            "liquidity": self.liquidity_manager.active(
                symbol
            ),
            "fair_value_gaps": self.fvg_manager.active(
                symbol
            ),
        }

        self._last_result[symbol] = result

        return result