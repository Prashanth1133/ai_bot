from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class NewsCategory(Enum):

    ETF = "etf"

    REGULATION = "regulation"

    LISTING = "listing"

    DELISTING = "delisting"

    HACK = "hack"

    PARTNERSHIP = "partnership"

    MACRO = "macro"

    FED = "fed"

    CPI = "cpi"

    FOMC = "fomc"

    WHALE = "whale"

    UNKNOWN = "unknown"


class Sentiment(Enum):

    VERY_BEARISH = -2

    BEARISH = -1

    NEUTRAL = 0

    BULLISH = 1

    VERY_BULLISH = 2


@dataclass(slots=True)
class NewsArticle:

    id: str

    source: str

    title: str

    summary: str

    content: str

    url: str

    published: datetime

    category: NewsCategory = NewsCategory.UNKNOWN

    sentiment: Sentiment = Sentiment.NEUTRAL

    impact: float = 0.0

    confidence: float = 0.0

    affected_assets: list[str] = field(default_factory=list)

    tags: list[str] = field(default_factory=list)

    embedding: list[float] | None = None