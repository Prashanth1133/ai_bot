from __future__ import annotations

from collections import defaultdict
import numpy as np


class MTFContextProvider:

    def __init__(self, mtf_manager):
        self.mtf_manager = mtf_manager

    def __call__(self, snapshot) -> None:
        analysis = self.mtf_manager.analyze(snapshot.symbol)
        snapshot.market["mtf"] = analysis


class SRContextProvider:

    def __init__(
        self,
        sr_engine,
        candle_manager,
    ):
        self.sr_engine = sr_engine
        self.candle_manager = candle_manager

    def __call__(self, snapshot) -> None:
        history = self.candle_manager.history(
            snapshot.symbol,
            snapshot.timeframe,
        )
        snapshot.indicators["support_resistance"] = self.sr_engine.analyze(history)


class PatternContextProvider:

    def __init__(
        self,
        pattern_engine,
        candle_manager,
    ):
        self.pattern_engine = pattern_engine
        self.candle_manager = candle_manager

    def __call__(self, snapshot) -> None:
        history = self.candle_manager.history(
            snapshot.symbol,
            snapshot.timeframe,
        )

        if len(history) < 5:
            snapshot.market["patterns"] = {
                "detected": [],
                "count": 0,
                "primary_pattern": "NONE",
                "primary_direction": "NEUTRAL",
                "primary_strength": 0.0,
            }
            return

        patterns = self.pattern_engine.detect(history)

        # Only patterns whose ending timestamp is <= current candle are allowed
        current_ts = getattr(history[-1], "open_time", None)
        causal_patterns = []

        for pattern in patterns:
            pattern_ts = getattr(
                pattern,
                "open_time",
                getattr(pattern, "timestamp", None),
            )
            if pattern_ts is None or current_ts is None or pattern_ts <= current_ts:
                causal_patterns.append(pattern)

        primary = causal_patterns[-1] if causal_patterns else None
        direction = "NEUTRAL"
        strength = 0.0

        if primary:
            raw_direction = getattr(primary, "direction", "NEUTRAL")
            direction = getattr(raw_direction, "value", str(raw_direction))
            direction = str(direction).upper()
            strength = float(
                getattr(
                    primary,
                    "confidence",
                    getattr(primary, "strength", 0.0),
                )
            )

        snapshot.market["patterns"] = {
            "detected": [
                (p.to_dict() if hasattr(p, "to_dict") else str(p))
                for p in causal_patterns
            ],
            "count": len(causal_patterns),
            "primary_pattern": (
                getattr(primary, "name", "NONE") if primary else "NONE"
            ),
            "primary_direction": direction,
            "primary_strength": float(np.clip(strength, 0.0, 1.0)),
        }


class SMCContextProvider:
    """Populates Smart Money Concepts into ContextSnapshot."""

    def __init__(
        self,
        smc_engine,
        candle_manager,
    ):
        self.smc_engine = smc_engine
        self.candle_manager = candle_manager

    def __call__(self, snapshot) -> None:

        history = self.candle_manager.history(
            snapshot.symbol,
            snapshot.timeframe,
        )

        if len(history) < 20:
            snapshot.smart_money = {
                "atr": 0.0,
                "structure": "NEUTRAL",
                "bos": False,
                "choch": False,
                "state": "RANGE",
                "active_order_blocks": 0,
                "active_liquidity_zones": 0,
                "active_fvgs": 0,
            }
            return

        smc_res = self.smc_engine.process(
            history
        )

        if smc_res is None:
            snapshot.smart_money = {
                "atr": 0.0,
                "structure": "NEUTRAL",
                "bos": False,
                "choch": False,
                "state": "RANGE",
                "active_order_blocks": 0,
                "active_liquidity_zones": 0,
                "active_fvgs": 0,
            }
            return

        bos = smc_res.get("bos")
        choch = smc_res.get("choch")

        bos_name = getattr(
            bos,
            "name",
            str(bos),
        )

        choch_name = getattr(
            choch,
            "name",
            str(choch),
        )

        snapshot.smart_money = {
            "atr": float(
                smc_res.get(
                    "atr",
                    0.0,
                )
            ),

            "structure": getattr(
                smc_res.get("structure"),
                "name",
                "NEUTRAL",
            ),

            "bos": (
                bos_name != "NONE"
            ),

            "choch": (
                choch_name != "NONE"
            ),

            "state": getattr(
                smc_res.get("state"),
                "name",
                "RANGE",
            ),

            "active_order_blocks": len(
                smc_res.get(
                    "order_blocks",
                    [],
                )
            ),

            "active_liquidity_zones": len(
                smc_res.get(
                    "liquidity",
                    [],
                )
            ),

            "active_fvgs": len(
                smc_res.get(
                    "fair_value_gaps",
                    [],
                )
            ),
        }


class OrderFlowContextProvider:

    def __init__(
        self,
        orderflow_engine,
        feature_engine=None,
    ):
        self.orderflow_engine = orderflow_engine
        self.feature_engine = feature_engine

    def __call__(self, snapshot) -> None:
        metrics = self.orderflow_engine.get_metrics(snapshot.symbol)
        buy = float(getattr(metrics, "buy_volume", 0.0) if metrics else 0.0)
        sell = float(getattr(metrics, "sell_volume", 0.0) if metrics else 0.0)
        cvd = float(getattr(metrics, "cvd", 0.0) if metrics else 0.0)
        delta = float(getattr(metrics, "delta", 0.0) if metrics else 0.0)

        # Historical dataset must not consume current/live order-book state
        imbalance = (buy - sell) / (buy + sell + 1e-12)

        snapshot.orderflow = {
            "cvd": cvd,
            "delta": delta,
            "buy_volume": buy,
            "sell_volume": sell,
            "bid_volume": buy,
            "ask_volume": sell,
            "imbalance": float(np.clip(imbalance, -1.0, 1.0)),
            "pressure": (
                "BUY_PRESSURE"
                if imbalance > 0.1
                else ("SELL_PRESSURE" if imbalance < -0.1 else "BALANCED")
            ),
        }


class NewsContextProvider:

    def __init__(
        self,
        news_processor=None,
    ):
        self.news_processor = news_processor

    def __call__(self, snapshot) -> None:
        if self.news_processor is None:
            raise RuntimeError(
                "Historical news provider is required. "
                "Do not inject neutral/synthetic news values."
            )

        result = self.news_processor.process(snapshot)
        if result is None:
            raise RuntimeError("Historical news provider returned no data.")

        snapshot.news = result


class VolumeProfileContextProvider:

    def __init__(
        self,
        volume_profile_engine,
        candle_manager,
    ):
        self.volume_profile_engine = volume_profile_engine
        self.candle_manager = candle_manager

    def __call__(self, snapshot) -> None:
        history = self.candle_manager.history(
            snapshot.symbol,
            snapshot.timeframe,
        )

        if len(history) < 20:
            snapshot.indicators["volume_profile"] = {
                "poc": 0.0,
                "vah": 0.0,
                "val": 0.0,
                "vwap": 0.0,
            }
            return

        result = self.volume_profile_engine.process(history)
        profile = result.get("profile", {})
        raw_vwap = result.get("vwap")

        def value(obj, key):
            if hasattr(obj, key):
                return float(getattr(obj, key) or 0.0)
            if isinstance(obj, dict):
                return float(obj.get(key, 0.0) or 0.0)
            return 0.0

        snapshot.indicators["volume_profile"] = {
            "poc": value(profile, "poc"),
            "vah": value(profile, "vah"),
            "val": value(profile, "val"),
            "vwap": float(raw_vwap or 0.0),
        }


class MarketRegimeContextProvider:

    def __init__(
        self,
        regime_engine,
    ):
        self.regime_engine = regime_engine

    def __call__(self, snapshot) -> None:
        mtf = snapshot.market.get("mtf", {})
        tf5 = mtf.get("timeframes", {}).get("5m", {})

        features = {
            "ema20": tf5.get("ema20", 0.0),
            "ema50": tf5.get("ema50", 0.0),
            "ema200": tf5.get("ema200", 0.0),
            "atr": tf5.get("atr", 0.0),
            "close": tf5.get("close", 0.0),
            "rsi": tf5.get("rsi", 50.0),
            "macd": 0.0,
            "smart_money_score": 0.5,
        }

        state = (
            self.regime_engine.process(features)
            if hasattr(self.regime_engine, "process")
            else None
        )

        if state is None:
            raise RuntimeError("Market regime provider returned no state.")

        snapshot.regime = {
            "name": str(state),
            "volatility": float(tf5.get("volatility", 0.0)),
        }


class DerivativesContextProvider:

    def __init__(
        self,
        derivatives_engine=None,
    ):
        self.derivatives_engine = derivatives_engine

    def __call__(self, snapshot) -> None:
        if self.derivatives_engine is None:
            raise RuntimeError("Historical derivatives provider is required.")

        result = self.derivatives_engine.process(
            snapshot,
            getattr(snapshot, "previous_oi", None),
        )

        if result is None:
            raise RuntimeError("Historical derivatives provider returned no data.")

        snapshot.derivatives = {
            "funding_rate": float(result.get("funding", 0.0)),
            "open_interest_change": float(result.get("open_interest", 0.0)),
            "taker_imbalance": float(result.get("taker_imbalance", 0.0)),
            "liquidation_cascade_flag": bool(result.get("liquidations", False)),
        }


class OnChainContextProvider:

    def __init__(
        self,
        onchain_processor=None,
    ):
        self.onchain_processor = onchain_processor

    def __call__(self, snapshot) -> None:
        if self.onchain_processor is None:
            raise RuntimeError("Historical on-chain provider is required.")

        result = self.onchain_processor.process(snapshot)
        if result is None:
            raise RuntimeError("Historical on-chain provider returned no data.")

        snapshot.onchain = result
