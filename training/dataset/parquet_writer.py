import pandas as pd


class DatasetWriter:

    def save(

        self,

        samples,

        filename

    ):

        rows = []

        for s in samples:

            rows.append({

                "symbol": s.symbol,

                "timeframe": s.timeframe,

                "timestamp": s.timestamp,

                "direction": s.direction,

                "confidence": s.confidence,

                "tp": s.tp,

                "sl": s.sl,

                "regime": s.regime,

                "sequence": s.sequence.tolist()

            })

        df = pd.DataFrame(rows)

        df.to_parquet(
            filename,
            index=False
        )