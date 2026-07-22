from dataclasses import dataclass


@dataclass(slots=True)
class MarketContext:

    trend: object

    volatility: str

    session: object

    score: float

    class ContextScorer:

    def score(

        self,

        trend,

        volatility,

        session

    ):

        score = 0

        if trend.name.startswith("STRONG"):

            score += 40

        elif trend.name in ("BULLISH", "BEARISH"):

            score += 20

        if volatility == "MEDIUM":

            score += 30

        elif volatility == "HIGH":

            score += 10

        else:

            score += 15

        if session.name == "OVERLAP":

            score += 30

        elif session.name == "LONDON":

            score += 20

        else:

            score += 10

        return MarketContext(

            trend,

            volatility,

            session,

            score

        )