from evaluation.production_evaluator import (
    ProductionEvaluator
)


def test_evaluator_accepts_saved_report():
    report = ProductionEvaluator().evaluate(
        {"accuracy": 98.54, "loss": 0.012, "confidence": 97.35}
    )
    assert report["accuracy"] == 98.54
