from evaluation.production_metrics import(
    ProductionMetrics
)


def test_production_metrics_summary():
    metrics = ProductionMetrics()
    metrics.update(150, 0.95)
    metrics.update(-50, 0.87)
    metrics.update(300, 0.93)
    assert metrics.summary()["total_pnl"] == 400.0
