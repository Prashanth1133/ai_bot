class AIController:

    """
    Central AI coordinator.
    """

    def __init__(

        self,
        ai_trader,
        autonomous_ai

    ):

        self.ai_trader = ai_trader

        self.autonomous_ai = (

            autonomous_ai

        )

        self.enabled = True

    def enable(self):

        self.enabled = True

    def disable(self):

        self.enabled = False

    def status(self):

        return {

            "enabled":

                self.enabled,

            "cycles":

                self.autonomous_ai
                .cycles

        }

    async def process(

        self,
        symbol,
        features,
        trade=None

    ):

        if not self.enabled:

            return None

        result = await (

            self.ai_trader

            .process(

                symbol,

                features

            )

        )

        self.autonomous_ai.step(

            features,

            trade

        )

        return result