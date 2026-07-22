from ai.live.engine import (
    LiveAI
)

engine = LiveAI()

response = engine.process(

    features=[
        0.1,
        0.2,
        1.1,
        0.5,
        55
    ],

    price=117000
)

print(
    response
)