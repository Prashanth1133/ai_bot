from decimal import Decimal

from paper.paper_engine import (
    PaperEngine
)

from backtest.portfolio import (
    BacktestPortfolio
)


def test_backtest():


    portfolio = (

        BacktestPortfolio()

    )


    portfolio.add_profit(

        Decimal("250")

    )


    portfolio.add_loss(

        Decimal("100")

    )


    result = (

        portfolio.summary()

    )


    print(result)


    assert result is not None


if __name__ == "__main__":

    test_backtest()