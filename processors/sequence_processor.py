from __future__ import annotations

from collections import defaultdict, deque

import numpy as np

from app.settings import settings
from logs.log_manager import pipeline_logger


class SequenceProcessor:
    """
    Maintains independent model sequences per symbol/timeframe.

    Historical data fills the sequence before live inference begins.
    """

    def __init__(self, bus):

        self.bus = bus

        self.buffers = defaultdict(
            lambda: deque(
                maxlen=settings.MODEL_SEQUENCE_LENGTH
            )
        )

    # ==========================================================
    # LIVE FEATURE VECTOR
    # ==========================================================

    async def on_feature_vector(self, vector_packet):

        sequence = self.prime(vector_packet)

        if sequence is None:
            return

        pipeline_logger.info(
            f"[SEQUENCE READY] "
            f"{vector_packet['symbol']} "
            f"{vector_packet['interval']} "
            f"shape={sequence.shape}"
        )

        await self.bus.publish(
            "feature_sequence",
            {
                "symbol": vector_packet["symbol"],
                "interval": vector_packet["interval"],
                "values": sequence,
            },
        )

    # ==========================================================
    # ADD LIVE VECTOR
    # ==========================================================

    def prime(self, vector_packet):

        values = np.asarray(
            vector_packet["values"],
            dtype=np.float32,
        )

        # -------------------------------------------------
        # 2D Sequence input (e.g. from rolling sequence buffer)
        # -------------------------------------------------
        if values.ndim == 2:

            if values.shape[1] != settings.MODEL_INPUT_DIM:

                raise ValueError(
                    f"Expected feature dim {settings.MODEL_INPUT_DIM}, "
                    f"got {values.shape[1]}"
                )

            if len(values) < settings.MODEL_SEQUENCE_LENGTH:
                return None

            sequence = values[-settings.MODEL_SEQUENCE_LENGTH:]

            return np.expand_dims(
                sequence,
                axis=0,
            )

        # -------------------------------------------------
        # 1D Single feature vector
        # -------------------------------------------------
        expected_shape = (
            settings.MODEL_INPUT_DIM,
        )

        if values.shape != expected_shape:

            raise ValueError(
                f"Expected {expected_shape} feature vector, "
                f"got {values.shape}"
            )

        key = (
            vector_packet["symbol"],
            vector_packet["interval"],
        )

        buffer = self.buffers[key]

        buffer.append(values)

        if len(buffer) < settings.MODEL_SEQUENCE_LENGTH:

            return None

        sequence = np.asarray(
            buffer,
            dtype=np.float32,
        )

        if sequence.shape != (
            settings.MODEL_SEQUENCE_LENGTH,
            settings.MODEL_INPUT_DIM,
        ):

            raise ValueError(
                f"Invalid sequence shape: "
                f"{sequence.shape}"
            )

        return np.expand_dims(
            sequence,
            axis=0,
        )

    # ==========================================================
    # HISTORICAL WARM-UP
    # ==========================================================

    def warmup(
        self,
        symbol,
        interval,
        vectors,
    ):

        key = (
            symbol,
            interval,
        )

        buffer = self.buffers[key]

        buffer.clear()

        expected_shape = (
            settings.MODEL_INPUT_DIM,
        )

        for vector in vectors:

            values = np.asarray(
                vector,
                dtype=np.float32,
            )

            if values.shape != expected_shape:

                raise ValueError(
                    f"Expected {expected_shape}, "
                    f"got {values.shape}"
                )

            buffer.append(values)

        pipeline_logger.info(
            f"[SEQUENCE WARMUP] "
            f"{symbol} "
            f"{interval} "
            f"{len(buffer)}/"
            f"{settings.MODEL_SEQUENCE_LENGTH}"
        )

        return len(buffer)
