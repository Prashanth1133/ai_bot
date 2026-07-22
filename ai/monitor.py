import time


class Monitor:

    def log(
        self,
        data
    ):

        print(
            f"[{time.time()}]"
            f" {data}"
        )