import logging
import uuid
from abc import ABC, abstractmethod

tx_context = dict()


class Writer(ABC):
    @abstractmethod
    def start(self, context):
        pass

    @abstractmethod
    def end(self, context):
        pass


class WriterOff(Writer):

    def start(self, context):
        pass

    def end(self, context):
        pass


class WriterOn(Writer):

    def start(self, context):
        logging.info(f"start {context['name']}: tx_id: {context['tx_id']}")

    def end(self, context):
        logging.info(f"start {context['name']}: tx_id: {context['tx_id']}")


class Logger:
    pid: bool
    logger: Writer

    def __init__(self, pid: uuid, on: bool = True):
        self.pid = pid
        self.logger = WriterOn() if on else WriterOff()

    def start(self, context):
        self.logger.start(context)

    def end(self, context):
        self.logger.end(context)
