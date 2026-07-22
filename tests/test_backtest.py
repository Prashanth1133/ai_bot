from backtest.engine import BacktestEngine


def test_backtest():

    engine=BacktestEngine()

    assert engine is not None