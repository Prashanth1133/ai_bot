from live.ai_trade_manager import (
    AITradeManager
)

manager = AITradeManager()

result = manager.decide(

    {

        "signal": "BUY",
        "confidence": 0.91

    },

    118500

)

print(result)