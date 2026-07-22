from __future__ import annotations


class TimeframeSelector:

    DEFAULT = (

        "1m",

        "5m",

        "15m",

        "1h",

        "4h",

    )

    def __init__(

        self,

        enabled=None,

    ):

        self.enabled = enabled or self.DEFAULT

    def selected(self):

        return self.enabled

    def contains(

        self,

        timeframe,

    ):

        return timeframe in self.enabled