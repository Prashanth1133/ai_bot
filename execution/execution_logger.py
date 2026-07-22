from __future__ import annotations

import logging


class ExecutionLogger:

    def __init__(
        self,
        name="execution",
    ):

        self.logger = logging.getLogger(name)

    def info(self, message):

        self.logger.info(message)

    def warning(self, message):

        self.logger.warning(message)

    def error(self, message):

        self.logger.error(message)

    def exception(
        self,
        message,
    ):

        self.logger.exception(message)