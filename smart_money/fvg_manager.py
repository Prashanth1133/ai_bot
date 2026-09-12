from __future__ import annotations

from collections import defaultdict
from smart_money.fvg_types import FVGStatus


class FVGManager:
    """
    Manages Fair Value Gaps with:
    - deterministic deduplication
    - directional fill detection
    - age-based expiration
    - bounded storage
    - active-gap cleanup
    """

    def __init__(
        self,
        max_gaps_per_symbol: int = 500,
        max_age_candles: int = 240,
    ):
        self.max_gaps_per_symbol = int(max_gaps_per_symbol)
        self.max_age_candles = int(max_age_candles)

        self.gaps = defaultdict(list)
        self._known = defaultdict(set)

    @staticmethod
    def _time(value):
        if value is None:
            return None
        try:
            return int(value)
        except (TypeError, ValueError):
            return None

    @classmethod
    def _gap_time(cls, gap):
        candle = getattr(gap, "candle", None)
        candle_time = cls._time(getattr(candle, "open_time", None))
        if candle_time is not None:
            return candle_time
        return cls._time(getattr(gap, "open_time", None))

    @staticmethod
    def _status_name(gap):
        status = getattr(gap, "status", None)
        return getattr(status, "name", str(status))

    @staticmethod
    def _gap_key(gap):
        symbol = str(getattr(gap, "symbol", "")).upper()
        candle = getattr(gap, "candle", None)
        candle_time = getattr(candle, "open_time", None)
        if candle_time is None:
            candle_time = getattr(gap, "open_time", None)

        lower = float(getattr(gap, "lower", 0.0))
        upper = float(getattr(gap, "upper", 0.0))

        return (
            symbol,
            candle_time,
            round(lower, 8),
            round(upper, 8),
        )

    def add(self, gap):
        if gap is None:
            return False

        symbol = str(getattr(gap, "symbol", "")).upper()
        if not symbol:
            return False

        key = self._gap_key(gap)
        if key in self._known[symbol]:
            return False

        self.gaps[symbol].append(gap)
        self._known[symbol].add(key)

        self._prune(symbol)
        return True

    def add_many(self, gaps):
        added = 0
        for gap in gaps or []:
            if self.add(gap):
                added += 1
        return added

    def update(self, symbol, price, current_time=None):
        symbol = str(symbol).upper()

        try:
            price = float(price)
        except (TypeError, ValueError):
            return

        if price <= 0:
            return

        current_time = self._time(current_time)
        gaps = self.gaps.get(symbol)
        if not gaps:
            return

        remaining = []

        for gap in gaps:
            if self._status_name(gap) != "OPEN":
                self._known[symbol].discard(self._gap_key(gap))
                continue

            gap_time = self._gap_time(gap)

            # Age expiration (240 candles = 4 hours)
            if current_time is not None and gap_time is not None:
                age_ms = current_time - gap_time
                max_age_ms = self.max_age_candles * 60_000
                if age_ms > max_age_ms:
                    self._known[symbol].discard(self._gap_key(gap))
                    continue

            try:
                lower = float(gap.lower)
                upper = float(gap.upper)
            except (AttributeError, TypeError, ValueError):
                self._known[symbol].discard(self._gap_key(gap))
                continue

            # Directional fill check
            gap_type = getattr(gap, "gap_type", None)
            gap_type_str = str(getattr(gap_type, "value", str(gap_type))).lower()

            is_filled = False
            if "bull" in gap_type_str:
                if price <= upper:
                    is_filled = True
            elif "bear" in gap_type_str:
                if price >= lower:
                    is_filled = True
            else:
                if lower <= price <= upper:
                    is_filled = True

            if is_filled:
                gap.status = FVGStatus.FILLED
                self._known[symbol].discard(self._gap_key(gap))
                continue

            remaining.append(gap)

        self.gaps[symbol] = remaining
        self._prune(symbol)

    def active(self, symbol):
        symbol = str(symbol).upper()
        gaps = self.gaps.get(symbol)
        if not gaps:
            return []

        return [
            gap
            for gap in gaps
            if self._status_name(gap) == "OPEN"
        ]

    def _prune(self, symbol):
        symbol = str(symbol).upper()
        gaps = self.gaps.get(symbol)
        if not gaps:
            return

        # Remove anything that is no longer open.
        open_gaps = [
            gap
            for gap in gaps
            if self._status_name(gap) == "OPEN"
        ]

        # Keep newest gaps only if storage exceeds the limit.
        if len(open_gaps) > self.max_gaps_per_symbol:
            open_gaps = open_gaps[-self.max_gaps_per_symbol:]

        self.gaps[symbol] = open_gaps
        self._known[symbol] = {
            self._gap_key(gap)
            for gap in open_gaps
        }

    def clear_symbol(self, symbol):
        symbol = str(symbol).upper()
        self.gaps.pop(symbol, None)
        self._known.pop(symbol, None)

    def reset(self):
        self.gaps.clear()
        self._known.clear()