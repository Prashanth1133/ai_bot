from loguru import logger

import sys

logger.remove()

logger.add(
    sys.stdout,
    level="INFO",
    colorize=True,
    enqueue=True
)

logger.add(
    "logs/cryptovision.log",
    rotation="50 MB",
    retention="30 days",
    enqueue=True,
    level="DEBUG"
)