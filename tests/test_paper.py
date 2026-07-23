from decimal import Decimal
from types import SimpleNamespace

from paper.paper_engine import PaperEngine


def test_paper():

    engine = PaperEngine()


    trade = SimpleNamespace(

        symbol="BTCUSDT",

        side="BUY",

        quantity=Decimal("0.01"),

        entry_price=Decimal("120000"),

        leverage=10,

        market_regime="TREND",

        pattern="BULL_FLAG",

        news_label="POSITIVE",

        session="US",

        confidence=0.94

    )


    risk = SimpleNamespace(

        adjusted_stop=Decimal("118000"),

        adjusted_target=Decimal("125000")

    )


    fill = engine.execute(

        trade,

        risk

    )


    assert fill is not None

    print(fill)
    

if __name__ == "__main__":

    test_paper()