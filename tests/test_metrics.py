from evaluation.production_metrics import(
    ProductionMetrics
)


metrics = ProductionMetrics()


metrics.update(

    150,
    0.95

)


metrics.update(

    -50,
    0.87

)


metrics.update(

    300,
    0.93

)


metrics.summary()