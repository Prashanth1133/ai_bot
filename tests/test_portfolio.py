from paper.portfolio_manager import (
    PortfolioManager
)


manager = PortfolioManager()


manager.update_profit(

    150

)


manager.update_profit(

    300

)


manager.update_loss(

    50

)


manager.summary()