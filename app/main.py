import asyncio

from app.logger import logger
from app.settings import settings

from core.market_engine import MarketEngine
from live.trade_manager import TradeManager
from exchange.binance_exchange import BinanceExchange
from live.portfolio_manager import PortfolioManager
from live.risk.risk_manager import RiskManager

async def run():

    logger.info("Initializing Market Engine...")

    engine = MarketEngine()
    exchange = BinanceExchange()
    risk_manager = RiskManager(settings)
    

    trade_manager = TradeManager(

        exchange,

        risk_manager,

    )

    portfolio_manager = PortfolioManager()

    # ----------------------------
    # Event Subscribers
    # ----------------------------

    async def print_trade(trade):
        logger.info(
            f"[TRADE] {trade.symbol:<10} "
            f"{trade.side:<4} "
            f"Price={trade.price} "
            f"Qty={trade.quantity}"
        )

    async def print_candle(candle):
        if candle.closed:
            logger.info(
                f"[CANDLE] {candle.symbol:<10} "
                f"{candle.interval:<4} "
                f"O:{candle.open} "
                f"H:{candle.high} "
                f"L:{candle.low} "
                f"C:{candle.close}"
            )

    async def print_orderflow(metrics):
        logger.info(
            f"[FLOW] "
            f"CVD={metrics.cvd} "
            f"Delta={metrics.delta}"
        )

    async def print_orderbook(book):
        logger.debug(
            f"[ORDERBOOK] {book.symbol} "
            f"Bids={len(book.bids)} "
            f"Asks={len(book.asks)}"
        )

    engine.bus.subscribe("trade", print_trade)
    engine.bus.subscribe("candle", print_candle)
    engine.bus.subscribe("orderbook", print_orderbook)
    engine.bus.subscribe("orderflow", print_orderflow)
    
    logger.success("Market Engine Started")

    await engine.start()

    await trade_manager.synchronize(

        portfolio_manager

    )

    stats = trade_manager.statistics()

    logger.info(

        f"Trades={stats['trades']} "

        f"WinRate={stats['win_rate']:.2%} "

        f"PF={stats['profit_factor']:.2f} "

        f"DD={stats['drawdown']:.2%}"

    )


def main():

    logger.info("=" * 60)
    logger.info(f"{settings.APP_NAME}")
    logger.info("Professional AI Quant Trading Platform")
    logger.info(f"Environment : {settings.ENV}")
    logger.info("=" * 60)

    try:
        asyncio.run(run())

    except KeyboardInterrupt:
        logger.warning("Application stopped by user.")

    except Exception as e:
        logger.exception(e)


if __name__ == "__main__":
    main()