from types import SimpleNamespace

from app.logger import logger
from app.settings import settings
from logs.log_manager import paper_logger
from paper_trading.journal import PaperTradeJournal
from paper_trading.trade_manager import TradeManager


class PaperTradeExecutor:
    def __init__(self, journal=None):
        self.trade_manager = TradeManager()
        self.journal = journal or PaperTradeJournal(settings.PAPER_JOURNAL_PATH)
        positions, balance = self.journal.recover(self.trade_manager.portfolio.balance)
        self.trade_manager.portfolio.positions = positions
        self.trade_manager.portfolio.balance = balance

    async def on_signal(self, signal):
        action = getattr(signal, "action", getattr(signal, "side", None))
        if action not in {"BUY", "SELL"}:
            return

        position = self.trade_manager.portfolio.positions.get(signal.symbol)
        if position and position["side"] == action:
            paper_logger.info(
                f"[PAPER IGNORED] "
                f"{signal.symbol} "
                f"already has {action} position"
            )
            return
        if position:
            self.trade_manager.close_position(signal)

        self.trade_manager.open_position(signal)
        self.journal.record(
            "OPEN",
            symbol=signal.symbol,
            side=action,
            entry_price=float(signal.entry_price),
            quantity=float(signal.quantity),
            take_profit=float(signal.take_profit),
            stop_loss=float(signal.stop_loss),
            confidence=float(signal.confidence),
            reversal=bool(signal.reversal),
            balance=float(self.trade_manager.portfolio.balance),
        )
        paper_logger.info(
            f"[PAPER] "
            f"{action} "
            f"{signal.symbol} "
            f"{signal.confidence}"
        )
        logger.info(
            f"[PAPER] opened {action} {signal.symbol} "
            f"entry={signal.entry_price:.6f} TP={signal.take_profit:.6f} "
            f"SL={signal.stop_loss:.6f} confidence={signal.confidence:.2%}"
        )

    async def on_trade(self, trade):
        position = self.trade_manager.portfolio.positions.get(trade.symbol)
        if position is None:
            return

        price = float(trade.price)
        is_long = position["side"] == "BUY"
        target_hit = price >= position["take_profit"] if is_long else price <= position["take_profit"]
        stop_hit = price <= position["stop_loss"] if is_long else price >= position["stop_loss"]
        if not (target_hit or stop_hit):
            return

        reason = "TP" if target_hit else "SL"
        completed = self.trade_manager.close_position(
            SimpleNamespace(symbol=trade.symbol, entry_price=price)
        )
        if completed:
            self.journal.record(
                "CLOSE",
                symbol=trade.symbol,
                side=completed["side"],
                entry_price=float(completed["entry"]),
                exit_price=float(completed["exit"]),
                quantity=float(completed["quantity"]),
                pnl=float(completed["pnl"]),
                exit_reason=reason,
                balance=float(self.trade_manager.portfolio.balance),
            )
            logger.info(
                f"[PAPER] {reason} {trade.symbol} exit={price:.6f} "
                f"PnL={completed['pnl']:.6f}"
            )


PaperExecutor = PaperTradeExecutor
