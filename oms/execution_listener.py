class ExecutionListener:

    def __init__(

        self,

        bus,

        order_manager,

    ):

        self.bus = bus

        self.manager = order_manager

        self.bus.subscribe(

            "execution",

            self.on_execution,

        )

    async def on_execution(

        self,

        execution,

    ):

        self.manager.completed(
            execution
        )