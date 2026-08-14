import json

from paper_trading.journal import PaperTradeJournal


def test_paper_journal_appends_json_records(tmp_path):
    path = tmp_path / "paper_trades.jsonl"
    PaperTradeJournal(path).record("OPEN", symbol="BTCUSDT", confidence=0.9)
    record = json.loads(path.read_text(encoding="utf-8"))
    assert record["event"] == "OPEN"
    assert record["symbol"] == "BTCUSDT"
