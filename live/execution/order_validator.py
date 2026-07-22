class OrderValidator:

    def validate(self, order):

        if order["quantity"] <= 0:

            raise ValueError(
                "Quantity must be positive."
            )

        return True