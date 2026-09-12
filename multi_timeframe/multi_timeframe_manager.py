from __future__ import annotations

from collections import defaultdict, deque
from dataclasses import dataclass
from typing import Any

import numpy as np

from indicators.ema import EMA
from indicators.rsi import RSI
from indicators.volatility import Volatility


class _IncrementalATR:

    def __init__(self, period: int = 14):
        self.period = int(period)
        self.reset()

    def reset(self) -> None:
        self.prev_close: float | None = None
        self.tr_values: deque[float] = deque(maxlen=self.period)
        self.atr: float | None = None

    def update(self, candle: Any) -> float | None:
        high = float(candle.high)
        low = float(candle.low)
        close = float(candle.close)

        if not all(np.isfinite(x) for x in (high, low, close)):
            return self.atr

        if high < low:
            return self.atr

        if self.prev_close is None:
            tr = high - low
        else:
            tr = max(
                high - low,
                abs(high - self.prev_close),
                abs(low - self.prev_close),
            )

        self.prev_close = close

        if not np.isfinite(tr):
            return self.atr

        if self.atr is None:
            self.tr_values.append(float(tr))

            if len(self.tr_values) < self.period:
                return None

            self.atr = float(np.mean(self.tr_values))
            return self.atr

        self.atr = (self.atr * (self.period - 1) + tr) / self.period
        return float(self.atr)

    def value(self) -> float:
        return float(self.atr) if self.atr is not None else 0.0


@dataclass
class _TimeframeState:
    atr: _IncrementalATR
    last_close: float = 0.0
    previous_close: float = 0.0
    ema20: float = 0.0
    ema50: float = 0.0
    ema200: float = 0.0
    ema20_ready: bool = False
    ema50_ready: bool = False
    ema200_ready: bool = False
    rsi: float = 50.0
    volatility: float = 0.0
    initialized: bool = False


class MultiTimeframeManager:

    TIMEFRAMES = (
        "1m",
        "5m",
        "15m",
        "1h",
        "4h",
    )

    EMA20_PERIOD = 20
    EMA50_PERIOD = 50
    EMA200_PERIOD = 200
    RSI_PERIOD = 14
    ATR_PERIOD = 14
    VOLATILITY_WINDOW = 20

    def __init__(
        self,
        history_size: int = 300,
    ):
        self.history_size = int(
            max(
                history_size,
                self.EMA200_PERIOD + 20,
            )
        )
        self.candles = defaultdict(
            lambda: deque(maxlen=self.history_size)
        )
        self._states: dict[tuple[str, str], _TimeframeState] = {}

    def _get_state(
        self,
        symbol: str,
        timeframe: str,
    ) -> _TimeframeState:
        key = (
            symbol.upper(),
            timeframe,
        )
        state = self._states.get(key)
        if state is None:
            state = _TimeframeState(
                atr=_IncrementalATR(self.ATR_PERIOD)
            )
            self._states[key] = state
        return state

    def _rebuild_state(
        self,
        symbol: str,
        timeframe: str,
        history: list,
    ) -> None:
        key = (
            symbol.upper(),
            timeframe,
        )
        state = _TimeframeState(
            atr=_IncrementalATR(self.ATR_PERIOD)
        )
        self._states[key] = state

        if not history:
            return

        ordered = sorted(
            history,
            key=lambda c: int(getattr(c, "open_time", 0)),
        )
        closes = np.asarray(
            [float(c.close) for c in ordered],
            dtype=np.float64,
        )

        if len(closes) == 0:
            return

        # Rebuild ATR exactly once
        for candle in ordered:
            state.atr.update(candle)

        state.last_close = float(closes[-1])

        if len(closes) >= 2:
            state.previous_close = float(closes[-2])

        if len(closes) >= self.EMA20_PERIOD:
            value = float(
                EMA(self.EMA20_PERIOD).latest(closes)
            )
            if np.isfinite(value):
                state.ema20 = value
                state.ema20_ready = True

        if len(closes) >= self.EMA50_PERIOD:
            value = float(
                EMA(self.EMA50_PERIOD).latest(closes)
            )
            if np.isfinite(value):
                state.ema50 = value
                state.ema50_ready = True

        if len(closes) >= self.EMA200_PERIOD:
            value = float(
                EMA(self.EMA200_PERIOD).latest(closes)
            )
            if np.isfinite(value):
                state.ema200 = value
                state.ema200_ready = True

        if len(closes) >= self.RSI_PERIOD:
            value = float(
                RSI(self.RSI_PERIOD).latest(closes)
            )
            if np.isfinite(value):
                state.rsi = float(np.clip(value, 0.0, 100.0))

        if len(closes) >= self.VOLATILITY_WINDOW:
            value = float(
                Volatility.calculate(
                    closes,
                    window=self.VOLATILITY_WINDOW,
                )
            )
            if np.isfinite(value):
                state.volatility = max(0.0, value)

        state.initialized = True

    def update_history(
        self,
        symbol: str,
        timeframe: str,
        candles_list: list,
    ) -> None:
        symbol = symbol.upper()
        if timeframe not in self.TIMEFRAMES:
            raise ValueError(f"Unsupported timeframe: {timeframe}")

        key = (
            symbol,
            timeframe,
        )
        ordered = sorted(
            [c for c in candles_list if getattr(c, "closed", True)],
            key=lambda c: int(getattr(c, "open_time", 0)),
        )

        # Deduplicate
        unique = []
        seen = set()
        for candle in ordered:
            ts = getattr(candle, "open_time", None)
            if ts in seen:
                continue
            seen.add(ts)
            unique.append(candle)

        unique = unique[-self.history_size :]
        self.candles[key].clear()
        self.candles[key].extend(unique)
        self._rebuild_state(symbol, timeframe, unique)

    def update_candle(
        self,
        candle,
    ) -> None:
        if not getattr(candle, "closed", True):
            return

        symbol = str(getattr(candle, "symbol", "")).upper()
        timeframe = str(getattr(candle, "interval", ""))

        if not symbol or timeframe not in self.TIMEFRAMES:
            return

        key = (
            symbol,
            timeframe,
        )
        history = self.candles[key]
        ts = getattr(candle, "open_time", None)

        if history:
            last_ts = getattr(history[-1], "open_time", None)
            if ts == last_ts:
                history[-1] = candle
                # Rebuild because the candle changed
                self._rebuild_state(symbol, timeframe, list(history))
                return
            if ts is not None and last_ts is not None and ts < last_ts:
                return

        history.append(candle)
        state = self._get_state(symbol, timeframe)

        if state.initialized:
            state.previous_close = state.last_close
            state.last_close = float(candle.close)
            state.atr.update(candle)

            closes = np.asarray(
                [float(c.close) for c in history],
                dtype=np.float64,
            )

            if len(closes) >= self.EMA20_PERIOD:
                value = float(
                    EMA(self.EMA20_PERIOD).latest(closes)
                )
                if np.isfinite(value):
                    state.ema20 = value
                    state.ema20_ready = True

            if len(closes) >= self.EMA50_PERIOD:
                value = float(
                    EMA(self.EMA50_PERIOD).latest(closes)
                )
                if np.isfinite(value):
                    state.ema50 = value
                    state.ema50_ready = True

            if len(closes) >= self.EMA200_PERIOD:
                value = float(
                    EMA(self.EMA200_PERIOD).latest(closes)
                )
                if np.isfinite(value):
                    state.ema200 = value
                    state.ema200_ready = True

            if len(closes) >= self.RSI_PERIOD:
                value = float(
                    RSI(self.RSI_PERIOD).latest(closes)
                )
                if np.isfinite(value):
                    state.rsi = float(np.clip(value, 0.0, 100.0))

            if len(closes) >= self.VOLATILITY_WINDOW:
                value = float(
                    Volatility.calculate(
                        closes,
                        window=self.VOLATILITY_WINDOW,
                    )
                )
                if np.isfinite(value):
                    state.volatility = max(0.0, value)
        else:
            self._rebuild_state(symbol, timeframe, list(history))

    def analyze_timeframe(
        self,
        symbol: str,
        timeframe: str,
    ) -> dict:
        symbol = symbol.upper()
        if timeframe not in self.TIMEFRAMES:
            raise ValueError(f"Unsupported timeframe: {timeframe}")

        history = self.candles[(symbol, timeframe)]
        state = self._get_state(symbol, timeframe)

        close = float(state.last_close)
        previous_close = float(state.previous_close)

        if previous_close > 0 and close > 0:
            return_1 = close / previous_close - 1.0
        else:
            return_1 = 0.0

        result = {
            "timeframe": timeframe,
            "trend": "NEUTRAL",
            "trend_score": 0.0,
            "close": close,
            "previous_close": previous_close,
            "return": float(return_1),
            "returns": float(return_1),
            "volume": (
                float(getattr(history[-1], "volume", 0.0))
                if history
                else 0.0
            ),
            "ema20": float(state.ema20),
            "ema50": float(state.ema50),
            "ema200": float(state.ema200),
            "ema200_ready": bool(state.ema200_ready),
            "rsi": float(state.rsi),
            "atr": float(state.atr.value()),
            "volatility": float(state.volatility),
        }

        if len(history) < self.EMA20_PERIOD:
            return result

        bullish = 0
        bearish = 0
        available = 0

        if state.ema20_ready:
            available += 1
            if close > state.ema20:
                bullish += 1
            else:
                bearish += 1

        if state.ema50_ready:
            available += 1
            if state.ema20 > state.ema50:
                bullish += 1
            else:
                bearish += 1

        if state.ema200_ready:
            available += 1
            if close > state.ema200:
                bullish += 1
            else:
                bearish += 1

        if state.rsi is not None:
            available += 1
            if state.rsi > 55:
                bullish += 1
            elif state.rsi < 45:
                bearish += 1

        if available == 0:
            return result

        score = (bullish - bearish) / available
        if score >= 0.5:
            trend = "BULLISH"
        elif score <= -0.5:
            trend = "BEARISH"
        else:
            trend = "NEUTRAL"

        result["trend"] = trend
        result["trend_score"] = float(np.clip(score, -1.0, 1.0))
        return result

    def analyze(
        self,
        symbol: str,
    ) -> dict:
        symbol = symbol.upper()
        tf_results = {}
        scores = []

        for timeframe in self.TIMEFRAMES:
            result = self.analyze_timeframe(
                symbol,
                timeframe,
            )
            tf_results[timeframe] = result
            scores.append(result["trend_score"])

        valid_scores = [x for x in scores if np.isfinite(x)]
        alignment = (
            float(np.mean(valid_scores)) if valid_scores else 0.0
        )

        if alignment >= 0.25:
            primary = "BULLISH"
        elif alignment <= -0.25:
            primary = "BEARISH"
        else:
            primary = "NEUTRAL"

        return {
            "symbol": symbol,
            "primary_trend": primary,
            "alignment_score": float(
                np.clip(abs(alignment), 0.0, 1.0)
            ),
            "directional_score": float(
                np.clip(alignment, -1.0, 1.0)
            ),
            "timeframes": tf_results,
        }

    def reset(
        self,
        symbol: str | None = None,
    ) -> None:
        if symbol is None:
            self.candles.clear()
            self._states.clear()
            return

        symbol = symbol.upper()
        keys = [key for key in self._states if key[0] == symbol]
        for key in keys:
            self._states.pop(key, None)
            self.candles.pop(key, None)
