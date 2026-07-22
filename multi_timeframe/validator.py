from __future__ import annotations


class MultiTimeframeValidator:

    REQUIRED = (

        "1m",

        "5m",

        "15m",

        "1h",

    )

    @classmethod
    def validate(

        cls,

        data,

    ):

        for tf in cls.REQUIRED:

            if tf not in data:

                return False

            if data[tf] is None:

                return False

        return True