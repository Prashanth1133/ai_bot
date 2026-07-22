import schedule
import time

from ai.auto_retrainer import (
    AutoRetrainer
)

trainer = (
    AutoRetrainer()
)

schedule.every().day.at(
    "00:00"
).do(
    trainer.retrain
)

while True:

    schedule.run_pending()

    time.sleep(
        1
    )