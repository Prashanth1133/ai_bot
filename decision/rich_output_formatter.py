from __future__ import annotations

from logs.log_manager import ai_logger, pipeline_logger


class RichSignalFormatter:
    """
    Formats the complete multi-factor Market Context and AI Decision into
    the rich human-auditable output block.
    """

    @staticmethod
    def format_signal(snapshot, signal=None, trade_signal=None) -> str:
        symbol = snapshot.symbol
        mtf = snapshot.market.get("mtf", {})
        tfs = mtf.get("timeframes", {})
        sr = snapshot.indicators.get("support_resistance", {})
        smc = snapshot.smart_money or {}
        patterns = snapshot.market.get("patterns", {})
        flow = snapshot.orderflow or {}
        news = snapshot.news or {}

        # Default values for formatting
        tf_4h = tfs.get("4h", {}).get("trend", "NEUTRAL")
        tf_1h = tfs.get("1h", {}).get("trend", "NEUTRAL")
        tf_15m = tfs.get("15m", {}).get("trend", "NEUTRAL")
        tf_5m = tfs.get("5m", {}).get("trend", "NEUTRAL")
        tf_1m = tfs.get("1m", {}).get("trend", "NEUTRAL")

        action = getattr(signal, "action", "HOLD") if signal else "HOLD"
        confidence = getattr(signal, "confidence", 0.0) if signal else 0.0
        entry = getattr(signal, "entry_price", tfs.get("5m", {}).get("close", 0.0)) if signal else tfs.get("5m", {}).get("close", 0.0)
        tp = getattr(signal, "take_profit", entry * 1.01) if signal else entry * 1.01
        sl = getattr(signal, "stop_loss", entry * 0.99) if signal else entry * 0.99

        tp1 = entry + (tp - entry) * 0.5
        tp2 = tp

        rr = abs(tp - entry) / max(abs(entry - sl), 1e-8)

        sep_thick = "=" * 44
        sep_thin = "-" * 44

        output = f"""
{sep_thick}
          {symbol} AI MARKET ANALYSIS
{sep_thick}
Signal:         {action}
Confidence:     {confidence * 100:.1f}%

Trend:
  4H:           {tf_4h}
  1H:           {tf_1h}
  15M:          {tf_15m}
  5M:           {tf_5m}
  1M:           {tf_1m}

MTF Alignment:  {mtf.get('primary_trend', 'NEUTRAL')} (Score: {mtf.get('alignment_score', 0.0):.2f})

Structure:
  CHoCH:        {'CONFIRMED' if smc.get('choch') else 'NONE'}
  BOS:          {'BEARISH' if smc.get('bos') else 'NONE'}

Momentum:
  Direction:    {tf_5m}
  RSI (5m):     {tfs.get('5m', {}).get('rsi', 50.0):.1f}

Candle:
  Pattern:      {patterns.get('primary_pattern', 'NONE')}
  Strength:     {patterns.get('primary_strength', 0.0):.2f}

Support:        {sr.get('nearest_support', 0.0):.2f} (Strength: {sr.get('support_strength', 0.0):.2f}, Dist: {sr.get('support_distance_pct', 0.0)*100:.2f}%)
Resistance:     {sr.get('nearest_resistance', 0.0):.2f} (Strength: {sr.get('resistance_strength', 0.0):.2f}, Dist: {sr.get('resistance_distance_pct', 0.0)*100:.2f}%)

Order Flow:
  Delta:        {flow.get('delta', 0.0):.2f}
  CVD:          {flow.get('cvd', 0.0):.2f}
  Book Imbal:   {flow.get('pressure', 'BALANCED')}

News:
  Sentiment:    {news.get('sentiment_label', 'NEUTRAL')} ({news.get('sentiment', 0.0):.2f})
  Impact:       {news.get('impact_level', 'LOW')} ({news.get('impact_score', 0.0):.2f})
  Relevance:    HIGH ({news.get('btc_relevance', 1.0):.2f})

{sep_thin}
Entry:          {entry:.2f}
Stop Loss:      {sl:.2f}
TP1:            {tp1:.2f}
TP2:            {tp2:.2f}
Risk/Reward:    1 : {rr:.1f}
Trade Quality:  {confidence:.2f}

Decision:       {'EXECUTE ' + action if action in ['BUY', 'SELL', 'SHORT', 'LONG'] else 'WAIT / HOLD'}
{sep_thick}
"""
        return output

    @classmethod
    def log_signal(cls, snapshot, signal=None, trade_signal=None) -> None:
        block = cls.format_signal(snapshot, signal, trade_signal)
        pipeline_logger.info(block)
        ai_logger.info(block)
