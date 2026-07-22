import pandas as pd


class ReplayEngine:

    """
    Replays historical candles
    through the complete system.
    """

    def __init__(

        self,

        market_engine

    ):

        self.engine = market_engine

    def replay(

        self,

        dataframe

    ):

        for _, row in dataframe.iterrows():

            candle = self.engine.create_candle(

                row

            )

            self.engine.process_candle(

                candle

            )