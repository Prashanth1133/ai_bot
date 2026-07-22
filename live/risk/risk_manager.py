from __future__ import annotations

from decimal import Decimal

from app.logger import logger

from live.risk.approval import ApprovalEngine

from live.risk.position_sizer import PositionSizer

from live.risk.drawdown_guard import DrawdownGuard
from live.risk.loss_guard import LossGuard
from live.risk.position_limits import PositionLimits
from live.risk.exposure_guard import ExposureGuard
from live.risk.funding_guard import FundingGuard
from live.risk.open_interest_guard import OpenInterestGuard
from live.risk.liquidity_guard import LiquidityGuard
from live.risk.spread_guard import SpreadGuard
from live.risk.volatility_guard import VolatilityGuard
from live.risk.correlation_guard import CorrelationGuard
from live.risk.margin_guard import MarginGuard
from live.risk.leverage_guard import LeverageGuard
from live.risk.news_guard import NewsGuard
from live.risk.circuit_breaker import CircuitBreaker

from live.risk.stop_loss import StopLossCalculator
from live.risk.take_profit import TakeProfitCalculator
from portfolio.portfolio_engine import PortfolioEngine

from live.risk.models import (
    TradeRequest,
    PortfolioState,
    MarketState,
    RiskDecision,
)



class RiskManager:

    """
    Central Risk Engine.

    Every trade must pass through this
    before reaching the execution engine.
    """

    def __init__(self, settings):

        self.settings = settings

        self.position_sizer = PositionSizer(
            settings.RISK_PER_TRADE
        )

        self.drawdown = DrawdownGuard(
            settings.MAX_DRAWDOWN
        )

        self.loss = LossGuard(
            settings.MAX_DAILY_LOSS,
            settings.MAX_WEEKLY_LOSS,
        )

        self.position = PositionLimits(
            settings.MAX_POSITION_PERCENT,
            settings.MAX_LEVERAGE,
        )

        self.exposure = ExposureGuard(
            settings.MAX_SYMBOL_EXPOSURE,
            settings.MAX_PORTFOLIO_EXPOSURE,
        )

        self.funding = FundingGuard(
            settings.MAX_FUNDING_RATE,
            settings.MIN_FUNDING_RATE,
        )

        self.open_interest = OpenInterestGuard(
            settings.MAX_OPEN_INTEREST_CHANGE,
        )

        self.liquidity = LiquidityGuard(
            settings.MINIMUM_BOOK_DEPTH,
        )

        self.spread = SpreadGuard(
            settings.MAX_SPREAD,
        )

        self.volatility = VolatilityGuard(
            settings.MIN_VOLATILITY,
            settings.MAX_VOLATILITY,
        )

        self.correlation = CorrelationGuard(
            settings.MAX_CORRELATION,
        )

        self.margin = MarginGuard(
            settings.MIN_MARGIN_RATIO,
        )

        self.leverage = LeverageGuard(
            settings.MAX_LEVERAGE,
        )

        self.news = NewsGuard(
            settings.NEWS_IMPACT_THRESHOLD,
        )

        self.breaker = CircuitBreaker(
            settings.MAX_INTRADAY_LOSS,
        )

        self.stop_loss = StopLossCalculator(
            settings.ATR_STOP_MULTIPLIER
        )

        self.take_profit = TakeProfitCalculator(
            settings.TAKE_PROFIT_LEVELS
        )

        self.portfolio_engine = PortfolioEngine()

        self.approval = ApprovalEngine()

    ######################################################################

    def evaluate(

        self,

        trade: TradeRequest,

        portfolio: PortfolioState,

        market: MarketState,

        previous_open_interest: Decimal,

        correlation: Decimal,

        daily_loss: Decimal,

        long: bool = True,

    ) -> RiskDecision:

        violations = []

        ##################################################################
        # Position Size
        ##################################################################

        quantity = self.position_sizer.calculate(

            portfolio,

            trade.entry_price,

            trade.stop_loss,

        )

        trade.quantity = quantity

        #####################################################

        portfolio_quantity = (

            self.portfolio_engine

            .allocator

            .allocate(

                portfolio,

                trade,

            )

        )

        trade.quantity = portfolio_quantity

        #####################################################

        ##################################################################
        # ATR Stop
        ##################################################################

        stop = self.stop_loss.atr_stop(

            trade.entry_price,

            market.atr,

            long,

        )

        trade.stop_loss = stop

        ##################################################################
        # Take Profit
        ##################################################################

        targets = self.take_profit.calculate(

            trade.entry_price,

            stop,

            long,

        )

        ##################################################################
        # Drawdown
        ##################################################################

        violation = self.drawdown.check(portfolio)

        if violation:
            violations.append(violation)

        ##################################################################
        # Loss
        ##################################################################

        violation = self.loss.check(portfolio)

        if violation:
            violations.append(violation)

        ##################################################################
        # Position Limit
        ##################################################################

        violation = self.position.check(
            trade,
            portfolio,
        )

        if violation:
            violations.append(violation)

        ##################################################################
        # Exposure
        ##################################################################

        violation = self.exposure.check(
            trade,
            portfolio,
        )

        if violation:
            violations.append(violation)

        ##################################################################
        # Funding
        ##################################################################

        violation = self.funding.check(
            market,
        )

        if violation:
            violations.append(violation)

        ##################################################################
        # Open Interest
        ##################################################################

        violation = self.open_interest.check(
            market.open_interest,
            previous_open_interest,
        )

        if violation:
            violations.append(violation)

        ##################################################################
        # Liquidity
        ##################################################################

        violation = self.liquidity.check(
            trade,
            market,
        )

        if violation:
            violations.append(violation)

        ##################################################################
        # Spread
        ##################################################################

        violation = self.spread.check(
            market,
        )

        if violation:
            violations.append(violation)

        ##################################################################
        # Volatility
        ##################################################################

        violation = self.volatility.check(
            market,
        )

        if violation:
            violations.append(violation)

        ##################################################################
        # Correlation
        ##################################################################

        violation = self.correlation.check(
            correlation,
        )

        if violation:
            violations.append(violation)

        ##################################################################
        # Margin
        ##################################################################

        violation = self.margin.check(
            trade,
            portfolio,
        )

        if violation:
            violations.append(violation)

        ##################################################################
        # Leverage
        ##################################################################

        violation = self.leverage.check(
            trade.leverage,
        )

        if violation:
            violations.append(violation)

        ##################################################################
        # News
        ##################################################################

        violation = self.news.check(
            market,
        )

        if violation:
            violations.append(violation)

        ##################################################################
        # Circuit Breaker
        ##################################################################

        if self.breaker.check(daily_loss):

            logger.warning(
                "Circuit Breaker Triggered."
            )

        ##################################################################
        # Final Decision
        ##################################################################

        decision = self.approval.approve(
            violations
        )

        decision.adjusted_quantity = quantity
        decision.adjusted_stop = stop

        if targets:
            decision.adjusted_target = targets[0].price

        ##################################################################
        # Logging
        ##################################################################

        if decision.approved:

            logger.success(
                "Trade Approved {} {} Qty={}",
                trade.symbol,
                trade.side,
                quantity,
            )

        else:

            logger.warning(
                "Trade Rejected {}",
                trade.symbol,
            )

            for violation in violations:

                logger.warning(
                    "{} -> {}",
                    violation.source,
                    violation.message,
                )

        return decision