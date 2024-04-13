from src.domain.message.message import Message
from src.domain.queue import Queue

__all__ = ["MessageQueue"]


class InnerQueue:
    queue: list[Message] = []

    def __dict__(self):
        return self.queue

    def append(self, message: Message):
        return self.queue.append(message)

    def pop(self):
        return self.queue.pop()

    def has_next(self):
        return len(self.queue) != 0


class MessageQueue(Queue):
    """ Singleton """

    _instance: InnerQueue = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(InnerQueue)
        return cls._instance

    def __dict__(self):
        return self._instance

    @classmethod
    def append(cls, message: Message):
        return cls._instance.append(message)

    @classmethod
    def pop(cls):
        return cls._instance.pop()

    @classmethod
    def has_next(cls):
        return cls._instance.has_next()
