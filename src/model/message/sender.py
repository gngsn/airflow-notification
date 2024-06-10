from abc import ABC
from itertools import islice
from typing import Iterator

from src.persistence.queue import NotificationQueue


def into_chuck(it: Iterator, n: int) -> Iterator[list]:
    while chunk := list(islice(it, n)):
        yield chunk


def run():
    chunk = 100
    senders = [ConsoleSender()]

    dequeue = NotificationQueue.dequeue(chunk)
    for sender in senders:
        for message in into_chuck(dequeue, chunk):
            code = sender.send(message)

        if code == -1:
            print("ERROR")
        if code == 0:
            print("Nothing happened")
        if code == 1:
            print("SUCCESS")


class Sender(ABC):
    def send(self, message) -> int:
        raise NotImplementedError()


class ConsoleSender(Sender):
    def send(self, message) -> int:
        print(message)
        return 1
