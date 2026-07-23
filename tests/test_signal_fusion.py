from production.signal_fusion import (
    SignalFusion
)


fusion = SignalFusion()


print(

    fusion.calculate(

        0.95,
        0.90,
        0.92,
        0.88,
        0.91,
        0.96

    )

)