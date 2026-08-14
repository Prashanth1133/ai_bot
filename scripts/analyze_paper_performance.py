"""Summarize completed paper trades recorded in logs/paper_trades.jsonl."""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

# Permit direct execution via ``python scripts/analyze_paper_performance.py``.
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.settings import settings


def load_closes(path: Path, days: int | None):
    if not path.is_file():
        return []
    cutoff = datetime.now(timezone.utc) - timedelta(days=days) if days else None
    records = []
    for line in path.read_text(encoding="utf-8").splitlines():
        try:
            record = json.loads(line)
            timestamp = datetime.fromisoformat(record["timestamp"])
        except (json.JSONDecodeError, KeyError, ValueError):
            continue
        if record.get("event") == "CLOSE" and (cutoff is None or timestamp >= cutoff):
            records.append(record)
    return records


def summarize(closes):
    initial = float(settings.INITIAL_CAPITAL)
    pnl = [float(item["pnl"]) for item in closes]
    gross_profit = sum(value for value in pnl if value > 0)
    gross_loss = abs(sum(value for value in pnl if value < 0))
    wins = sum(value > 0 for value in pnl)
    equity = initial
    peak = equity
    maximum_drawdown = 0.0
    for value in pnl:
        equity += value
        peak = max(peak, equity)
        maximum_drawdown = max(maximum_drawdown, (peak - equity) / peak if peak else 0.0)
    return {
        "completed_trades": len(pnl),
        "wins": wins,
        "losses": sum(value < 0 for value in pnl),
        "win_rate_pct": (wins / len(pnl) * 100) if pnl else 0.0,
        "net_pnl": sum(pnl),
        "profit_pct": (sum(pnl) / initial * 100) if initial else 0.0,
        "gross_profit": gross_profit,
        "gross_loss": gross_loss,
        "profit_factor": (gross_profit / gross_loss) if gross_loss else None,
        "max_drawdown_pct": maximum_drawdown * 100,
        "ending_equity": equity,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--days", type=int, default=14)
    parser.add_argument("--journal", default="logs/paper_trades.jsonl")
    args = parser.parse_args()
    result = summarize(load_closes(Path(args.journal), args.days))
    print(f"Paper performance: last {args.days} days")
    for key, value in result.items():
        if isinstance(value, float):
            value = f"{value:.4f}"
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()
