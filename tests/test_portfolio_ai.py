from ai.portfolio_manager import (
    PortfolioManager
)


manager = PortfolioManager()


manager.add(

    "BTCUSDT",

    "BUY",

    0.05

)


manager.add(

    "ETHUSDT",

    "BUY",

    1.50

)


print(

    manager.total()

)