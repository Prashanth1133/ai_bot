from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path


class PaperTradeJournal:
    """Append-only, restart-safe journal for paper-trading events."""

    def __init__(self, path: str = "logs/paper_trades.jsonl"):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def record(self, event: str, **data) -> None:
        payload = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "event": event,
            **data,
        }
        with self.path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(payload, separators=(",", ":")) + "\n")

    def recover(self, initial_balance: float):
        """Rebuild active positions and balance from a previous journal."""
        positions = {}
        balance = initial_balance
        if not self.path.is_file():
            return positions, balance
        for line in self.path.read_text(encoding="utf-8").splitlines():
            try:
                record = json.loads(line)
            except json.JSONDecodeError:
                continue
            if "balance" in record:
                balance = float(record["balance"])
            symbol = record.get("symbol")
            if record.get("event") == "OPEN" and symbol:
                positions[symbol] = {
                    "entry": float(record["entry_price"]),
                    "quantity": float(record["quantity"]),
                    "side": record["side"],
                    "take_profit": float(record["take_profit"]),
                    "stop_loss": float(record["stop_loss"]),
                }
            elif record.get("event") == "CLOSE" and symbol:
                positions.pop(symbol, None)
        return positions, balance
