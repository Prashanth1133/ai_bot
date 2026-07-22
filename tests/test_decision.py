from decision.decision_engine import DecisionEngine

from models.prediction import Prediction


def test_decision():

    engine=DecisionEngine()

    prediction=Prediction(

        symbol="BTCUSDT",

        action="BUY",

        confidence=0.9,

        probability_buy=0.9,

        probability_sell=0.05,

        probability_hold=0.05,

        stop_loss=100,

        take_profit=120,

    )

    result=engine.decide(prediction)

    assert result is not None