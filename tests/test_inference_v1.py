from production.production_inference import (
    ProductionInference
)


engine = ProductionInference()


print(

    engine.predict(

        {

        "transformer":0.96,

        "confidence":0.94,

        "sentiment":0.93,

        "social":0.92,

        "news":0.91,

        "whale":0.95,

        "volatility":0.30,

        "trend":0.90

        }

    )

)