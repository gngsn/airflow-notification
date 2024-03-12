import uuid
from enum import Enum
from typing import Callable

import pendulum

from src.monitor.logger import Logger


class BatchExecutionStatus(Enum):
    RUNNING: str = 'running'
    PENDING: str = 'pending'
    DONE: str = 'done'
    ERROR: str = 'error'


class Watcher:
    """
        Python method 모니터링
    """
    _uuid: uuid
    _logger: Logger

    context: dict

    def __init__(self, on_logging=True):
        self._uuid = uuid.uuid4()
        self._logger = Logger(self._uuid, on=on_logging)
        self.context = {
            "id": self._uuid,
        }

    def watch(
            self,
            func: Callable,
    ):
        def wrapper(*args, **kargs):
            self.context["name"] = func.__name__
            self.start()

            try:
                return func(*args, **kargs)
            except Exception as e:
                self.done(e)
            finally:
                self.done()

        return wrapper

    def start(self, start_date=pendulum.now()):
        self.context['start_date'] = start_date
        self._logger.start(self._uuid)

    def done(self,
             error: str | None = None,
             end_date=pendulum.now(),
             ):
        self.context['end_date'] = end_date

        if error:
            self.context['error'] = error
            self.context['is_success'] = False
        else:
            self.context['is_success'] = True

        self._logger.end(self._uuid)
