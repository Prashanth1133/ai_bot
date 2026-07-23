class PositionManager:


    def calculate(

        self,
        balance,
        risk,

        leverage=1

    ):


        size = (

            balance*

            risk*

            leverage

        )


        return round(

            size,

            2

        )