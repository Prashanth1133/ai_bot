from enum import Enum
from datetime import datetime, timezone


class TradingSession(Enum):

    ASIA = "Asia"

    LONDON = "London"

    NEW_YORK = "New York"

    OVERLAP = "London/New York"


class SessionAnalyzer:

    def current(self):

        now = datetime.now(timezone.utc).hour

        if 0 <= now < 8:
            return TradingSession.ASIA

        if 8 <= now < 13:
            return TradingSession.LONDON

        if 13 <= now < 17:
            return TradingSession.OVERLAP

        return TradingSession.NEW_YORK