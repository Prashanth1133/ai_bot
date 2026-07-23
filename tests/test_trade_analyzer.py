from paper.trade_analyzer import (
    TradeAnalyzer
)


analyzer = TradeAnalyzer()


analyzer.update(

    150,
    0.92

)


analyzer.update(

    300,
    0.96

)


analyzer.update(

    -40,
    0.88

)


analyzer.summary()