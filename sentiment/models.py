from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True)
class SocialPost:

    id: str

    platform: str

    author: str

    text: str

    timestamp: datetime

    likes: int = 0

    reposts: int = 0

    replies: int = 0

    views: int = 0

    followers: int = 0

    sentiment: float = 0.0

    influence: float = 0.0

    embedding: list[float] | None = None

    mentioned_assets: list[str] | None = None