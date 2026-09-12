from __future__ import annotations

from dataclasses import dataclass
import numpy as np

from dataset.labels import (
    DirectionLabel,
    RegimeLabel,
    ReversalLabel,
    LabelConfig,
)


def compute_structural_reversal(
    close_prices: np.ndarray | list[float],
    atr_pct: float,
    current_index: int,
    lookback_minutes: int = 60,
    future_horizon_minutes: int = 60,
    min_prior_move_atr: float = 1.0,
    min_future_move_atr: float = 0.75,
    min_directional_ratio: float = 0.55,
    retrace_fraction: float = 0.30,
    min_bars: int = 20,
) -> float:

    prices = np.asarray(
        close_prices,
        dtype=np.float64,
    )

    n = len(prices)

    if n == 0:
        return 0.0

    if current_index < lookback_minutes:
        return 0.0

    if current_index + future_horizon_minutes >= n:
        return 0.0

    if not np.isfinite(atr_pct) or atr_pct <= 0:
        return 0.0

    prior_start = current_index - lookback_minutes
    prior_end = current_index

    future_start = current_index
    future_end = current_index + future_horizon_minutes

    prior = prices[
        prior_start:prior_end + 1
    ]

    future = prices[
        future_start:future_end + 1
    ]

    if len(prior) < min_bars:
        return 0.0

    if len(future) < min_bars:
        return 0.0

    if not np.all(np.isfinite(prior)):
        return 0.0

    if not np.all(np.isfinite(future)):
        return 0.0

    prior_move = prior[-1] - prior[0]

    prior_return = (
        prior[-1] / prior[0]
    ) - 1.0

    prior_threshold = (
        min_prior_move_atr * atr_pct
    )

    # ---------------------------------------------------------
    # PRIOR TREND
    # ---------------------------------------------------------

    if prior_return >= prior_threshold:
        prior_direction = 1

    elif prior_return <= -prior_threshold:
        prior_direction = -1

    else:
        return 0.0

    prior_changes = np.diff(prior)

    if prior_direction > 0:
        prior_ratio = float(
            np.mean(prior_changes > 0)
        )
    else:
        prior_ratio = float(
            np.mean(prior_changes < 0)
        )

    if prior_ratio < min_directional_ratio:
        return 0.0

    # ---------------------------------------------------------
    # FUTURE OPPOSITE EXCURSION
    # ---------------------------------------------------------

    future_return = (
        future[-1] / future[0]
    ) - 1.0

    future_changes = np.diff(future)

    # Bullish prior -> bearish reversal
    if prior_direction > 0:

        future_extreme = float(
            np.min(future)
        )

        opposite_move = (
            future_extreme - future[0]
        ) / future[0]

        if opposite_move > -(
            min_future_move_atr * atr_pct
        ):
            return 0.0

        retracement = (
            prior[-1] - future_extreme
        )

        required_retrace = (
            abs(prior_move) * retrace_fraction
        )

        if retracement < required_retrace:
            return 0.0

    # Bearish prior -> bullish reversal
    else:

        future_extreme = float(
            np.max(future)
        )

        opposite_move = (
            future_extreme - future[0]
        ) / future[0]

        if opposite_move < (
            min_future_move_atr * atr_pct
        ):
            return 0.0

        retracement = (
            future_extreme - prior[-1]
        )

        required_retrace = (
            abs(prior_move) * retrace_fraction
        )

        if retracement < required_retrace:
            return 0.0

    # ---------------------------------------------------------
    # FUTURE DIRECTIONAL CONFIRMATION
    # ---------------------------------------------------------

    if prior_direction > 0:

        future_ratio = float(
            np.mean(future_changes < 0)
        )

    else:

        future_ratio = float(
            np.mean(future_changes > 0)
        )

    if future_ratio < 0.50:
        return 0.0

    return 1.0


@dataclass(slots=True)
class LabelResult:
    direction: int
    reversal: float
    regime: int

    # Multi-horizon returns
    future_return_15m: float
    future_return_30m: float
    future_return_1h: float
    future_return_4h: float

    # Path extremes
    max_future_return_15m: float
    min_future_return_15m: float
    max_future_return_1h: float
    min_future_return_1h: float
    max_future_return_4h: float
    min_future_return_4h: float

    # Dynamic TP / SL
    take_profit: float
    stop_loss: float

    # Boundary extremes
    future_high: float
    future_low: float


class LabelEngine:

    def __init__(self, config: LabelConfig | None = None):
        self.config = config or LabelConfig()

    def generate(
        self,
        closes: np.ndarray,
        highs: np.ndarray,
        lows: np.ndarray,
        index: int,
        atr: float,
    ) -> LabelResult | None:
        cfg = self.config

        closes = np.asarray(closes, dtype=np.float64)
        highs = np.asarray(highs, dtype=np.float64)
        lows = np.asarray(lows, dtype=np.float64)
        n = len(closes)

        h15 = index + cfg.horizon_15m
        h30 = index + cfg.horizon_30m
        h60 = index + cfg.horizon_1h
        h240 = index + cfg.horizon_4h

        if h240 >= n or index < 0:
            return None

        entry = float(closes[index])
        if entry <= 0:
            return None

        atr_pct = float(atr) / entry
        if not np.isfinite(atr_pct) or atr_pct <= 0:
            return None

        # -----------------------------------------------------
        # 1. MULTI-HORIZON FORWARD RETURNS
        # -----------------------------------------------------
        r15 = (float(closes[h15]) - entry) / entry
        r30 = (float(closes[h30]) - entry) / entry
        r60 = (float(closes[h60]) - entry) / entry
        r240 = (float(closes[h240]) - entry) / entry

        # -----------------------------------------------------
        # 2. FUTURE PATH SLICES
        # -----------------------------------------------------
        slice_15_highs = highs[index + 1 : h15 + 1]
        slice_15_lows = lows[index + 1 : h15 + 1]

        slice_60_highs = highs[index + 1 : h60 + 1]
        slice_60_lows = lows[index + 1 : h60 + 1]

        slice_240_highs = highs[index + 1 : h240 + 1]
        slice_240_lows = lows[index + 1 : h240 + 1]

        if len(slice_15_highs) == 0 or len(slice_60_highs) == 0 or len(slice_240_highs) == 0:
            return None

        # 15m extremes
        max_r15 = float(np.max(slice_15_highs) - entry) / entry
        min_r15 = float(np.min(slice_15_lows) - entry) / entry

        # 1h extremes
        max_r60 = float(np.max(slice_60_highs) - entry) / entry
        min_r60 = float(np.min(slice_60_lows) - entry) / entry

        # 4h extremes
        max_r240 = float(np.max(slice_240_highs) - entry) / entry
        min_r240 = float(np.min(slice_240_lows) - entry) / entry

        # -----------------------------------------------------
        # 3. FUTURE-PATH FIRST-TOUCH DIRECTION LABEL
        # -----------------------------------------------------
        up_threshold = max(cfg.min_direction_return, atr_pct * cfg.buy_atr_multiplier)
        down_threshold = max(cfg.min_direction_return, atr_pct * cfg.sell_atr_multiplier)

        first_up_bar = None
        first_down_bar = None

        for offset in range(len(slice_60_highs)):
            bar_high_ret = (slice_60_highs[offset] - entry) / entry
            bar_low_ret = (entry - slice_60_lows[offset]) / entry

            if first_up_bar is None and bar_high_ret >= up_threshold:
                first_up_bar = offset

            if first_down_bar is None and bar_low_ret >= down_threshold:
                first_down_bar = offset

            if first_up_bar is not None and first_down_bar is not None:
                break

        if first_up_bar is not None and (first_down_bar is None or first_up_bar < first_down_bar):
            direction = DirectionLabel.BUY
        elif first_down_bar is not None and (first_up_bar is None or first_down_bar < first_up_bar):
            direction = DirectionLabel.SELL
        elif r60 >= up_threshold:
            direction = DirectionLabel.BUY
        elif r60 <= -down_threshold:
            direction = DirectionLabel.SELL
        else:
            direction = DirectionLabel.HOLD

        # -----------------------------------------------------
        # 4. STRUCTURAL REVERSAL
        # -----------------------------------------------------
        reversal = compute_structural_reversal(
            close_prices=closes,
            atr_pct=atr_pct,
            current_index=index,
            lookback_minutes=cfg.reversal_lookback_minutes,
            future_horizon_minutes=cfg.reversal_future_horizon_minutes,
            min_prior_move_atr=cfg.reversal_min_prior_move_atr,
            min_future_move_atr=cfg.reversal_min_future_move_atr,
            min_directional_ratio=cfg.reversal_min_directional_ratio,
            retrace_fraction=cfg.reversal_retrace_fraction,
            min_bars=cfg.reversal_min_bars,
        )

        # -----------------------------------------------------
        # 5. MARKET REGIME (4H)
        # -----------------------------------------------------
        regime_threshold = max(cfg.min_regime_return, atr_pct * cfg.regime_atr_threshold)
        if r240 >= regime_threshold:
            regime = RegimeLabel.BULL
        elif r240 <= -regime_threshold:
            regime = RegimeLabel.BEAR
        else:
            regime = RegimeLabel.RANGE

        # -----------------------------------------------------
        # 6. DYNAMIC TP / SL (Path-derived with ATR bounds)
        # -----------------------------------------------------
        tp = float(np.clip(
            max(max_r60, atr_pct * cfg.tp_atr_multiplier),
            cfg.min_tp_pct,
            cfg.max_tp_pct,
        ))

        sl = float(np.clip(
            max(abs(min_r60), atr_pct * cfg.sl_atr_multiplier),
            cfg.min_sl_pct,
            cfg.max_sl_pct,
        ))

        return LabelResult(
            direction=int(direction),
            reversal=float(reversal),
            regime=int(regime),
            future_return_15m=float(r15),
            future_return_30m=float(r30),
            future_return_1h=float(r60),
            future_return_4h=float(r240),
            max_future_return_15m=float(max_r15),
            min_future_return_15m=float(min_r15),
            max_future_return_1h=float(max_r60),
            min_future_return_1h=float(min_r60),
            max_future_return_4h=float(max_r240),
            min_future_return_4h=float(min_r240),
            take_profit=tp,
            stop_loss=sl,
            future_high=float(np.max(slice_60_highs)),
            future_low=float(np.min(slice_60_lows)),
        )