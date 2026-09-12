from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from typing import Optional

import numpy as np
import pandas as pd


@dataclass
class IntelligencePoint:
    orderflow_cvd: float = 0.0
    orderflow_delta: float = 0.0
    orderflow_buy_volume: float = 0.0
    orderflow_sell_volume: float = 0.0
    orderbook_imbalance: float = 0.0

    derivatives_funding_rate: float = 0.0
    derivatives_oi_change: float = 0.0
    derivatives_taker_imbalance: float = 0.0

    news_sentiment: float = 0.0
    news_impact_score: float = 0.0
    news_btc_relevance: float = 0.0

    onchain_whale_score: float = 0.0
    onchain_exchange_net_flow: float = 0.0


class HistoricalIntelligence:
    """
    Historical intelligence alignment layer.

    Every timestamp must receive a value.

    External historical sources are loaded when available.
    Candle-derived microstructure proxies are used only
    for fields that cannot be recovered from OHLCV.
    """

    def __init__(
        self,
        candles,
        derivatives=None,
        news=None,
        onchain=None,
        orderbook=None,
    ):
        self.candles = candles
        self.derivatives = derivatives if derivatives is not None else pd.DataFrame()
        self.news = news if news is not None else pd.DataFrame()
        self.onchain = onchain if onchain is not None else pd.DataFrame()
        self.orderbook = orderbook if orderbook is not None else pd.DataFrame()

        self._cvd = 0.0
        self._history_delta = deque(maxlen=120)

    # =========================================================
    # CANDLE HELPERS
    # =========================================================

    @staticmethod
    def _get(candle, name, default=0.0):
        if isinstance(candle, dict):
            value = candle.get(name, default)
        else:
            value = getattr(candle, name, default)

        try:
            return float(value)
        except Exception:
            return float(default)

    # =========================================================
    # CANDLE MICROSTRUCTURE PROXY
    # =========================================================

    def _orderflow_from_candle(self, candle):
        open_price = self._get(candle, "open")
        close_price = self._get(candle, "close")
        high = self._get(candle, "high")
        low = self._get(candle, "low")
        volume = self._get(candle, "volume")

        # Extract taker buy volume if directly available on candle
        taker_buy_vol = self._get(candle, "taker_buy_volume", -1.0)

        if volume <= 0:
            return (0.0, 0.0, 0.0, 0.0)

        if taker_buy_vol >= 0.0 and taker_buy_vol <= volume:
            buy_volume = taker_buy_vol
            sell_volume = max(0.0, volume - taker_buy_vol)
            delta = buy_volume - sell_volume
        else:
            candle_range = max(high - low, 1e-12)
            body = close_price - open_price
            pressure = np.clip(body / candle_range, -1.0, 1.0)
            buy_volume = volume * (0.5 + 0.5 * pressure)
            sell_volume = volume * (0.5 - 0.5 * pressure)
            delta = buy_volume - sell_volume

        self._cvd += delta
        return (
            float(self._cvd),
            float(delta),
            float(buy_volume),
            float(sell_volume),
        )

    # =========================================================
    # ORDERBOOK PROXY
    # =========================================================

    def _orderbook_value(self, timestamp):
        if self.orderbook.empty:
            return None

        df = self.orderbook
        if "timestamp" not in df.columns:
            return None

        idx = (
            pd.to_datetime(df["timestamp"], unit="ms", errors="coerce")
            <= pd.to_datetime(timestamp, unit="ms", errors="coerce")
        )

        if not idx.any():
            return None

        row = df.loc[idx].iloc[-1]
        if {"bid_volume", "ask_volume"}.issubset(row.index):
            bid = float(row["bid_volume"])
            ask = float(row["ask_volume"])
            total = bid + ask
            if total > 0:
                return (bid - ask) / total

        return None

    # =========================================================
    # DERIVATIVES
    # =========================================================

    def _derivatives_value(self, timestamp, candle=None):
        if not self.derivatives.empty and "timestamp" in self.derivatives.columns:
            df = self.derivatives
            t = pd.to_datetime(timestamp, unit="ms", errors="coerce")
            times = pd.to_datetime(df["timestamp"], unit="ms", errors="coerce")
            mask = times <= t

            if mask.any():
                row = df.loc[mask].iloc[-1]
                funding = float(row.get("funding_rate", 0.0))
                oi_change = float(row.get("open_interest_change", 0.0))
                taker = float(row.get("taker_imbalance", 0.0))
                return (funding, oi_change, taker)

        # Microstructure causal proxy if external series unobserved
        if candle is not None:
            open_price = self._get(candle, "open")
            close_price = self._get(candle, "close")
            volume = self._get(candle, "volume")
            ret_proxy = (close_price - open_price) / max(open_price, 1e-8) if open_price > 0 else 0.0

            funding_proxy = float(np.clip(ret_proxy * 0.01 + 0.0001, -0.002, 0.002))
            oi_proxy = float(np.clip(ret_proxy * 2.0, -0.1, 0.1))
            taker_proxy = float(np.clip(ret_proxy * 100.0, -1.0, 1.0))
            return (funding_proxy, oi_proxy, taker_proxy)

        return (0.0, 0.0, 0.0)

    # =========================================================
    # NEWS
    # =========================================================

    def _news_value(self, timestamp, candle=None):
        if not self.news.empty and "timestamp" in self.news.columns:
            df = self.news
            t = pd.to_datetime(timestamp, unit="ms", errors="coerce")
            times = pd.to_datetime(df["timestamp"], unit="ms", errors="coerce")
            mask = times <= t

            if mask.any():
                rows = df.loc[mask]
                cutoff = t - pd.Timedelta(hours=24)
                rows = rows[times.loc[rows.index] >= cutoff]

                if not rows.empty:
                    sentiment = float(rows["sentiment"].mean() if "sentiment" in rows else 0.0)
                    impact = float(rows["impact_score"].max() if "impact_score" in rows else 0.0)
                    relevance = float(rows["btc_relevance"].max() if "btc_relevance" in rows else 0.0)
                    return (sentiment, impact, relevance)

        if candle is not None:
            open_price = self._get(candle, "open")
            close_price = self._get(candle, "close")
            high = self._get(candle, "high")
            low = self._get(candle, "low")

            range_pct = (high - low) / max(open_price, 1e-8) if open_price > 0 else 0.0
            ret_pct = (close_price - open_price) / max(open_price, 1e-8) if open_price > 0 else 0.0

            sentiment = float(np.tanh(ret_pct * 50.0))
            impact = float(np.clip(range_pct * 100.0, 0.0, 1.0))
            relevance = float(np.clip(0.8 + 0.2 * abs(sentiment), 0.5, 1.0))
            return (sentiment, impact, relevance)

        return (0.0, 0.0, 0.0)

    # =========================================================
    # ONCHAIN
    # =========================================================

    def _onchain_value(self, timestamp, candle=None):
        if not self.onchain.empty and "timestamp" in self.onchain.columns:
            df = self.onchain
            t = pd.to_datetime(timestamp, unit="ms", errors="coerce")
            times = pd.to_datetime(df["timestamp"], unit="ms", errors="coerce")
            mask = times <= t

            if mask.any():
                row = df.loc[mask].iloc[-1]
                whale = float(row.get("whale_score", 0.0))
                exchange_flow = float(row.get("exchange_net_flow", 0.0))
                return (whale, exchange_flow)

        if candle is not None:
            open_price = self._get(candle, "open")
            close_price = self._get(candle, "close")
            volume = self._get(candle, "volume")
            ret_pct = (close_price - open_price) / max(open_price, 1e-8) if open_price > 0 else 0.0

            whale = float(np.clip(0.5 + 0.5 * np.tanh(ret_pct * 20.0), 0.0, 1.0))
            exchange_flow = float(np.tanh(-ret_pct * 10.0))
            return (whale, exchange_flow)

        return (0.0, 0.0)

    # =========================================================
    # MAIN
    # =========================================================

    def get(self, candle):
        timestamp = self._get(candle, "close_time", self._get(candle, "open_time", self._get(candle, "timestamp")))

        (
            cvd,
            delta,
            buy_volume,
            sell_volume,
        ) = self._orderflow_from_candle(candle)

        orderbook = self._orderbook_value(timestamp)

        if orderbook is None:
            open_price = self._get(candle, "open")
            close_price = self._get(candle, "close")

            if open_price > 0:
                orderbook = float(np.tanh((close_price - open_price) / open_price * 1000.0))
            else:
                orderbook = 0.0

        (
            funding,
            oi_change,
            taker,
        ) = self._derivatives_value(timestamp, candle)

        (
            sentiment,
            impact,
            relevance,
        ) = self._news_value(timestamp, candle)

        (
            whale,
            exchange_flow,
        ) = self._onchain_value(timestamp, candle)

        return IntelligencePoint(
            orderflow_cvd=cvd,
            orderflow_delta=delta,
            orderflow_buy_volume=buy_volume,
            orderflow_sell_volume=sell_volume,
            orderbook_imbalance=orderbook,
            derivatives_funding_rate=funding,
            derivatives_oi_change=oi_change,
            derivatives_taker_imbalance=taker,
            news_sentiment=sentiment,
            news_impact_score=impact,
            news_btc_relevance=relevance,
            onchain_whale_score=whale,
            onchain_exchange_net_flow=exchange_flow,
        )
