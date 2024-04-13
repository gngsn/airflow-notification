from abc import ABC, abstractmethod

from src.model.message.message import Message


class Queue(ABC):
    @abstractmethod
    def append(self, message: Message):
        raise NotImplementedError

    @abstractmethod
    def pop(self) -> Message:
        raise NotImplementedError
