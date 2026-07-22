class CapitalAllocator:

    def allocate(

        self,

        available_capital,

        confidence,

        risk,

    ):

        confidence = max(

            0.0,

            min(

                confidence,

                1.0,

            ),

        )

        risk = max(

            risk,

            1e-6,

        )

        return (

            available_capital

            * confidence

        ) / risk