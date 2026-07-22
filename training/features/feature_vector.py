from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class FeatureVector:

    symbol: str

    timestamp: int

    # -----------------------------
    # Price
    # -----------------------------

    open: float
    high: float
    low: float
    close: float
    volume: float

    # -----------------------------
    # Smart Money
    # -----------------------------

    bos: int
    choch: int
    liquidity_sweep: int
    order_block: int
    fair_value_gap: int

    # -----------------------------
    # Order Flow
    # -----------------------------

    delta: float
    cvd: float
    imbalance: float
    absorption: float

    # -----------------------------
    # Order Book
    # -----------------------------

    spread: float
    bid_volume: float
    ask_volume: float
    depth_ratio: float

    # -----------------------------
    # Technical
    # -----------------------------

    atr: float
    rsi: float
    ema20: float
    ema50: float
    ema200: float
    vwap: float

    # -----------------------------
    # Volatility
    # -----------------------------

    volatility: float

    # -----------------------------
    # Regime
    # -----------------------------

    market_regime: int

    # -----------------------------
    # News
    # -----------------------------

    sentiment: float

    news_impact: float