class SignalRouter:

    """
    Routes signals
    to subscribers.
    """

    def __init__(self):

        self.routes = {}

    def subscribe(

        self,
        signal,
        callback

    ):

        if signal not in self.routes:

            self.routes[signal] = []

        self.routes[signal].append(

            callback

        )

    async def publish(

        self,
        signal,
        payload

    ):

        if signal not in self.routes:

            return

        for callback in self.routes[signal]:

            await callback(

                payload

            )