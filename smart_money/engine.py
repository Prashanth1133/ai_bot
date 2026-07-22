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

    def __init__(self):

        self.atr = ATRCalculator()

        self.swing = AdaptiveSwingDetector()

        self.structure = MarketStructure()

        self.bos = BreakOfStructure()

        self.choch = ChangeOfCharacter()

        self.state = StateEngine()

        self.order_blocks = OrderBlockDetector()

        self.block_manager = OrderBlockManager()

        self.liquidity = LiquidityDetector()

        self.liquidity_manager = LiquidityManager()

        self.fvg_detector = FairValueGapDetector()

        self.fvg_manager = FVGManager()

    def process(self, candles):

        if len(candles) < 20:

            return None

        latest = candles[-1]

        symbol = latest.symbol

        atr = self.atr.update(latest)

        if atr is None:

            return None

        swings = self.swing.detect(

            candles,

            atr

        )

        if len(swings) < 2:

            return None

        structure = self.structure.analyze(

            swings

        )

        bos = self.bos.detect(

            structure

        )

        choch = self.choch.detect(

            structure

        )

        state = self.state.update(

            symbol,

            structure.name

        )

        blocks = self.order_blocks.detect(

            candles,

            atr

        )

        fvgs = self.fvg_detector.detect(candles)

        for gap in fvgs:

            self.fvg_manager.add(gap)

        self.fvg_manager.update(

            symbol,

            latest.close

        )

        zones = self.liquidity.detect(candles)

        for zone in zones:

            self.liquidity_manager.add(zone)

        self.liquidity_manager.update(

            symbol,

            latest.close

        )

        for block in blocks:

            self.block_manager.add(block)

        self.block_manager.update(

            symbol,

            latest.close

        )

        return {

            "symbol": symbol,

            "atr": atr,

            "swings": swings,

            "structure": structure,

            "bos": bos,

            "choch": choch,

            "state": state,

            "order_blocks": self.block_manager.active(symbol),

            "liquidity": self.liquidity_manager.active(symbol),

            "fair_value_gaps": self.fvg_manager.active(symbol),

        }