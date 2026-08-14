from decision.ensemble import EnsembleEngine
from decision.signal_ranker import SignalRanker
from decision.market_filter import MarketFilter
from decision.trade_validator import TradeValidator
from ai.meta.meta_engine import MetaEngine
from logs.log_manager import pipeline_logger


class DecisionEngine:

    def __init__(self):

        self.ensemble = EnsembleEngine()

        self.ranker = SignalRanker()

        self.filter = MarketFilter()

        self.validator = TradeValidator()

        self.meta = MetaEngine()

    def decide(self, signal):

        if signal is None:
            return None

        # -------------------------------------------------
        # Preserve original AI direction
        # -------------------------------------------------

        ai_action = getattr(
            signal,
            "action",
            None,
        )

        # -------------------------------------------------
        # Decision layer
        # -------------------------------------------------

        signal = self.ensemble.evaluate(
            signal
        )

        signal = self.meta.evaluate(
            signal
        )

        # -------------------------------------------------
        # Direction must NEVER change
        # -------------------------------------------------

        decision_action = getattr(
            signal,
            "side",
            None,
        )

        if decision_action is None:
            decision_action = ai_action

        if decision_action != ai_action:

            pipeline_logger.warning(
                f"[DIRECTION MISMATCH] "
                f"AI={ai_action} "
                f"DECISION={decision_action}"
            )

            return None

        signal.action = ai_action
        signal.side = ai_action

        # -------------------------------------------------
        # Market filter
        # -------------------------------------------------

        if not self.filter.allow(signal):

            pipeline_logger.info(
                f"[DECISION REJECTED] "
                f"{signal.symbol} "
                f"market filter"
            )

            return None

        # -------------------------------------------------
        # Trade validator
        # -------------------------------------------------

        if not self.validator.validate(signal):

            pipeline_logger.info(
                f"[DECISION REJECTED] "
                f"{signal.symbol} "
                f"trade validator"
            )

            return None

        pipeline_logger.info(
            f"[DECISION ACCEPTED] "
            f"{signal.symbol} "
            f"action={signal.action} "
            f"confidence={signal.confidence:.4f}"
        )

        return signal