def create_label(
    current_price,
    future_price,
    threshold=0.003
):

    change = (
        future_price - current_price
    ) / current_price

    if change > threshold:
        return 1

    if change < -threshold:
        return -1

    return 0