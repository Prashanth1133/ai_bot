from __future__ import annotations

from collections import defaultdict, deque

from app.settings import settings
from features.feature_builder import FeatureBuilder
from logs.log_manager import pipeline_logger


class FeatureProcessor:
    """
    Converts closed candles into model-compatible feature sequences.

    Pipeline:

        Closed Candle
            ↓
        FeatureBuilder
            ↓
        11-feature vector
            ↓
        rolling sequence
            ↓
        feature_vector event
            ↓
        LiveSignalEngine

    Historical/live candles are maintained independently
    for each symbol and timeframe.
    """

    def __init__(self, feature_store, bus):

        self.store = feature_store
        self.bus = bus

        self.feature_builder = FeatureBuilder()

        # -------------------------------------------------
        # Candle history used by FeatureBuilder
        # -------------------------------------------------

        self.candles = defaultdict(
            lambda: deque(
                maxlen=settings.FEATURE_LOOKBACK
            )
        )

        # -------------------------------------------------
        # AI sequence buffer
        #
        # key:
        #     (symbol, timeframe)
        #
        # value:
        #     rolling feature vectors
        # -------------------------------------------------

        self.sequences = defaultdict(
            lambda: deque(
                maxlen=settings.MODEL_SEQUENCE_LENGTH
            )
        )

    # =====================================================
    # LIVE CLOSED CANDLE
    # =====================================================

    async def on_closed_candle(self, candle):

        if not candle.closed:
            return

        if candle.interval != settings.MODEL_TIMEFRAME:
            return

        pipeline_logger.info(
            f"[CLOSED CANDLE] "
            f"{candle.symbol} "
            f"{candle.interval}"
        )

        packet = self.ingest_closed_candle(
            candle
        )

        if packet is None:
            return

        sequence = packet["values"]

        pipeline_logger.info(
            f"[FEATURE PROCESSOR] "
            f"{candle.symbol} "
            f"feature_count={len(sequence[-1])} "
            f"sequence_length={len(sequence)}"
        )

        # -------------------------------------------------
        # Sequence not ready yet
        # -------------------------------------------------

        if len(sequence) < settings.MODEL_SEQUENCE_LENGTH:

            pipeline_logger.info(
                f"[AI WARMUP] "
                f"{candle.symbol} "
                f"{len(sequence)}/"
                f"{settings.MODEL_SEQUENCE_LENGTH}"
            )

            return

        # -------------------------------------------------
        # AI sequence ready
        # -------------------------------------------------

        pipeline_logger.info(
            f"[AI READY] "
            f"{candle.symbol} "
            f"sequence="
            f"{len(sequence)}x"
            f"{len(sequence[-1])}"
        )

        await self.bus.publish(
            "feature_vector",
            packet,
        )

    # =====================================================
    # LIVE CANDLE INGESTION
    # =====================================================

    def ingest_closed_candle(self, candle):

        if not candle.closed:
            return None

        if candle.interval != settings.MODEL_TIMEFRAME:
            return None

        key = (
            candle.symbol,
            candle.interval,
        )

        # -------------------------------------------------
        # Maintain candle history
        # -------------------------------------------------

        self.candles[key].append(
            candle
        )

        # -------------------------------------------------
        # Build current feature vector
        # -------------------------------------------------

        vector = self.feature_builder.build_training_compatible(
            self.candles[key]
        )

        if vector is None:
            return None

        # -------------------------------------------------
        # Validate feature dimension
        # -------------------------------------------------

        if len(vector) != settings.MODEL_INPUT_DIM:

            raise RuntimeError(
                f"Expected "
                f"{settings.MODEL_INPUT_DIM} features "
                f"got {len(vector)} "
                f"for {candle.symbol}"
            )

        # -------------------------------------------------
        # Add vector to rolling AI sequence
        # -------------------------------------------------

        self.sequences[key].append(
            vector
        )

        # -------------------------------------------------
        # Convert sequence to list
        # -------------------------------------------------

        sequence = list(
            self.sequences[key]
        )

        return {
            "symbol": candle.symbol,
            "interval": candle.interval,
            "values": sequence,
        }

    # =====================================================
    # HISTORICAL WARM-UP
    # =====================================================

    def build_historical_vector(self, candle):

        if not candle.closed:
            return None

        if candle.interval != settings.MODEL_TIMEFRAME:
            return None

        key = (
            candle.symbol,
            candle.interval,
        )

        self.candles[key].append(
            candle
        )

        vector = self.feature_builder.build_training_compatible(
            self.candles[key]
        )

        if vector is None:
            return None

        if len(vector) != settings.MODEL_INPUT_DIM:

            raise RuntimeError(
                f"Expected "
                f"{settings.MODEL_INPUT_DIM} features "
                f"got {len(vector)}"
            )

        # Historical vectors also warm the AI sequence.

        self.sequences[key].append(
            vector
        )

        return vector