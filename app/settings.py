
from decimal import Decimal
from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    # ==================================================
    # Application
    # ==================================================

    APP_NAME: str = "Quantitative AI Platform"
    ENV: str = "development"
    LOG_LEVEL: str = "INFO"

    # ==================================================
    # Database
    # ==================================================

    DATABASE: str = "sqlite:///cryptovision.db"

    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379

    # ==================================================
    # Binance
    # ==================================================

    BINANCE_WS: str = "wss://fstream.binance.com/stream"
    BINANCE_REST: str = "https://fapi.binance.com"

    BINANCE_API_KEY: str = ""
    BINANCE_SECRET_KEY: str = ""

    # ==================================================
    # Trading
    # ==================================================

    DEFAULT_SYMBOL: str = "BTCUSDT"
    DEFAULT_TIMEFRAME: str = "5m"

    PAPER_TRADING: bool = True
    ENABLE_LIVE_TRADING: bool = False

    # ==================================================
    # Risk Management
    # ==================================================

    RISK_PER_TRADE: Decimal = Decimal("0.01")

    MAX_DRAWDOWN: Decimal = Decimal("0.15")
    MAX_DAILY_LOSS: Decimal = Decimal("0.03")
    MAX_WEEKLY_LOSS: Decimal = Decimal("0.10")

    MAX_SYMBOL_EXPOSURE: Decimal = Decimal("0.20")
    MAX_PORTFOLIO_EXPOSURE: Decimal = Decimal("0.70")

    MAX_POSITION_PERCENT: Decimal = Decimal("0.10")
    
    MAX_LEVERAGE: int = 10

    ATR_STOP_MULTIPLIER: Decimal = Decimal("2.0")
    TRAILING_STOP_MULTIPLIER: Decimal = Decimal("1.5")

    MIN_RISK_REWARD: Decimal = Decimal("2.5")

    # ==================================================
    # Market Filters
    # ==================================================

    MAX_FUNDING_RATE: Decimal = Decimal("0.0005")
    MIN_FUNDING_RATE: Decimal = Decimal("-0.001")

    MAX_OPEN_INTEREST_CHANGE: Decimal = Decimal("0.15")

    MINIMUM_BOOK_DEPTH: Decimal = Decimal("3")

    MAX_SPREAD: Decimal = Decimal("0.0008")
    MAX_SPREAD_PERCENT: Decimal = Decimal("0.001")

    MIN_VOLATILITY: Decimal = Decimal("0.002")
    MAX_VOLATILITY: Decimal = Decimal("0.08")

    MAX_CORRELATION: Decimal = Decimal("0.90")

    # ==================================================
    # Execution Filters
    # ==================================================

    MIN_ORDERBOOK_LIQUIDITY: Decimal = Decimal("50000")

    MAX_SLIPPAGE_PERCENT: Decimal = Decimal("0.002")

    MIN_MARGIN_RATIO: Decimal = Decimal("0.20")

    MAX_INTRADAY_LOSS: Decimal = Decimal("0.03")

    # ==================================================
    # Funding / OI
    # ==================================================

    MAX_OI_CHANGE: Decimal = Decimal("0.10")

    # ==================================================
    # News & Sentiment
    # ==================================================

    NEWS_BLACKOUT_MINUTES: int = 30

    MIN_NEWS_SCORE: float = -0.60
    MIN_SENTIMENT_SCORE: float = -0.50

    NEWS_IMPACT_THRESHOLD: float = 0.80

    # ==================================================
    # AI
    # ==================================================

    MODEL_PATH: str = "models/checkpoints/latest.pt"

    DEVICE: str = "cpu"

    CONFIDENCE_THRESHOLD: float = 0.85

    # ==================================================
    # Features
    # ==================================================

    FEATURE_LOOKBACK: int = 200

    ATR_PERIOD: int = 14

    RSI_PERIOD: int = 14

    EMA_FAST: int = 20
    EMA_SLOW: int = 50
    EMA_TREND: int = 200

    # ==================================================
    # Order Flow
    # ==================================================

    ORDERFLOW_HISTORY: int = 5000

    # ==================================================
    # Smart Money
    # ==================================================

    SWING_LOOKBACK: int = 20

    ORDERBLOCK_HISTORY: int = 200

    FVG_HISTORY: int = 200

    # ==================================================
    # Take Profit Levels
    # ==================================================

    TAKE_PROFIT_LEVELS: List[Decimal] = [
        Decimal("1"),
        Decimal("2"),
        Decimal("3"),
        Decimal("5"),
    ]

    # ==================================================
    # Logging
    # ==================================================

    SAVE_SIGNALS: bool = True
    SAVE_TRADES: bool = True
    SAVE_FEATURES: bool = True
    SAVE_PREDICTIONS: bool = True

    # ==================================================
    # Backtesting
    # ==================================================

    INITIAL_CAPITAL: Decimal = Decimal("10000")

    MAKER_FEE: Decimal = Decimal("0.0002")
    TAKER_FEE: Decimal = Decimal("0.0005")

    # ==================================================
    # Pydantic
    # ==================================================

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
        case_sensitive=True,
    )


settings = Settings()

