from ai.production_manager import (
    ProductionManager
)


manager = ProductionManager()


prediction = {

    "signal":"BUY",

    "confidence":0.93,

    "take_profit":0.045,

    "stop_loss":0.015

}


result = manager.decision(

    prediction

)


print("\n")

print(

    "SIGNAL :",

    result["signal"]

)


print(

    "CONFIDENCE :",

    result["confidence"]

)


print(

    "APPROVED :",

    result["approved"]

)


print(

    "ACTION :",

    result["action"]

)


print(

    "TAKE PROFIT :",

    result["tp"]

)


print(

    "STOP LOSS :",

    result["sl"]

)

print("\n")