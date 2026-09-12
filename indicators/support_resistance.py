from __future__ import annotations

import numpy as np


class SupportResistanceEngine:

    def __init__(
        self,
        window: int = 5,
        tolerance_pct: float = 0.0015,
        max_lookback: int = 200,
        min_touch_separation: int = 5,
        level_merge_tolerance: float = 0.001,
        recency_decay: float = 30.0,
    ):
        self.window = int(window)
        self.tolerance_pct = float(tolerance_pct)
        self.max_lookback = int(max_lookback)
        self.min_touch_separation = int(min_touch_separation)
        self.level_merge_tolerance = float(level_merge_tolerance)
        self.recency_decay = float(recency_decay)

        self.last_breakout_level: float | None = None
        self.last_breakdown_level: float | None = None

    def reset(self):
        self.last_breakout_level = None
        self.last_breakdown_level = None

    def analyze(
        self,
        candles: list,
    ) -> dict:
        if not candles:
            return {
                "nearest_support": 0.0,
                "nearest_resistance": 0.0,
                "support_distance_pct": 0.0,
                "resistance_distance_pct": 0.0,
                "support_strength": 0.0,
                "resistance_strength": 0.0,
                "touch_count_support": 0,
                "touch_count_resistance": 0,
                "breakout_status": False,
                "breakdown_status": False,
                "support_zone": (
                    0.0,
                    0.0,
                ),
                "resistance_zone": (
                    0.0,
                    0.0,
                ),
            }

        candles = candles[-self.max_lookback :]
        highs = np.asarray(
            [float(c.high) for c in candles],
            dtype=np.float64,
        )
        lows = np.asarray(
            [float(c.low) for c in candles],
            dtype=np.float64,
        )
        closes = np.asarray(
            [float(c.close) for c in candles],
            dtype=np.float64,
        )
        opens = np.asarray(
            [float(getattr(c, "open", c.close)) for c in candles],
            dtype=np.float64,
        )

        price = float(closes[-1])
        if not np.isfinite(price) or price <= 0:
            return self.analyze([])

        w = min(
            self.window,
            max(1, len(candles) // 4),
        )
        swing_highs = []
        swing_lows = []

        for i in range(w, len(candles) - w):
            high_window = highs[i - w : i + w + 1]
            low_window = lows[i - w : i + w + 1]

            if highs[i] >= np.max(high_window):
                swing_highs.append(highs[i])

            if lows[i] <= np.min(low_window):
                swing_lows.append(lows[i])

        previous_price = (
            float(closes[-2])
            if len(closes) >= 2
            else price
        )

        prev_supports = [
            x for x in swing_lows
            if x < previous_price
        ]

        prev_resistances = [
            x for x in swing_highs
            if x > previous_price
        ]

        prev_support = (
            max(prev_supports)
            if prev_supports
            else previous_price * 0.98
        )

        prev_resistance = (
            min(prev_resistances)
            if prev_resistances
            else previous_price * 1.02
        )

        breakout = (
            previous_price <= prev_resistance
            and price > prev_resistance
        )

        breakdown = (
            previous_price >= prev_support
            and price < prev_support
        )

        if breakout:
            self.last_breakout_level = prev_resistance

        if breakdown:
            self.last_breakdown_level = prev_support

        supports = [x for x in swing_lows if x < price]
        resistances = [x for x in swing_highs if x > price]

        support = max(supports) if supports else price * 0.98
        resistance = min(resistances) if resistances else price * 1.02

        def count_touches_and_reactions(level: float, is_support: bool) -> tuple[int, int, int]:
            if level <= 0 or len(highs) == 0:
                return 0, 0, -1
            distances = np.minimum(
                np.abs(highs - level),
                np.abs(lows - level),
            ) / level
            near_mask = distances <= self.tolerance_pct
            touches = 0
            reactions = 0
            last_touch_idx = -1
            in_touch = False
            separation = self.min_touch_separation

            for idx, is_near in enumerate(near_mask):
                if is_near:
                    last_touch_idx = idx
                    if not in_touch and separation >= self.min_touch_separation:
                        touches += 1
                        in_touch = True
                        separation = 0
                        # Check reaction: price bounced away in the expected direction
                        if is_support:
                            # Downward test followed by upward rejection
                            if idx + 1 < len(closes) and (closes[idx + 1] > closes[idx] or closes[idx] >= opens[idx]):
                                reactions += 1
                        else:
                            # Upward test followed by downward rejection
                            if idx + 1 < len(closes) and (closes[idx + 1] < closes[idx] or closes[idx] <= opens[idx]):
                                reactions += 1
                    elif not in_touch and touches == 0:
                        touches += 1
                        in_touch = True
                        separation = 0
                        if is_support and closes[idx] >= opens[idx]:
                            reactions += 1
                        elif not is_support and closes[idx] <= opens[idx]:
                            reactions += 1
                else:
                    if in_touch:
                        in_touch = False
                    separation += 1

            return touches, reactions, last_touch_idx

        support_touches, support_reactions, sup_last_idx = count_touches_and_reactions(support, is_support=True)
        resistance_touches, resistance_reactions, res_last_idx = count_touches_and_reactions(resistance, is_support=False)

        def compute_strength(touches: int, reactions: int, last_idx: int) -> float:
            if touches == 0 or last_idx < 0:
                return 0.0
            touch_score = min(float(touches) / 10.0, 1.0)
            reaction_score = min(float(reactions) / 5.0, 1.0)
            bars_since_last_touch = float(len(candles) - 1 - last_idx)
            recency_score = float(np.exp(-bars_since_last_touch / max(self.recency_decay, 1.0)))
            strength = 0.40 * touch_score + 0.40 * reaction_score + 0.20 * recency_score
            return float(np.clip(strength, 0.0, 1.0))

        support_strength = compute_strength(support_touches, support_reactions, sup_last_idx)
        resistance_strength = compute_strength(resistance_touches, resistance_reactions, res_last_idx)

        support_distance = (support - price) / price
        resistance_distance = (resistance - price) / price

        return {
            "nearest_support": float(support),
            "nearest_resistance": float(resistance),
            "support_distance_pct": float(support_distance),
            "resistance_distance_pct": float(resistance_distance),
            "support_strength": support_strength,
            "resistance_strength": resistance_strength,
            "touch_count_support": support_touches,
            "touch_count_resistance": resistance_touches,
            "breakout_status": breakout,
            "breakdown_status": breakdown,
            "support_zone": (
                float(support * (1.0 - self.tolerance_pct)),
                float(support * (1.0 + self.tolerance_pct)),
            ),
            "resistance_zone": (
                float(resistance * (1.0 - self.tolerance_pct)),
                float(resistance * (1.0 + self.tolerance_pct)),
            ),
        }
