from abc import ABC
from typing import Iterator

from src.persistence.queue import NotificationQueue


def chunk(it: Iterator, size: int):
    iterator = iter(it)
    done = False
    while not done:
        c = []
        for _ in range(size):
            try:
                c.append(next(iterator))
            except StopIteration:
                done = True
                break
        if c:
            yield c


def run():
    chunk_size = 100
    senders = [ConsoleSender()]

    dequeue = NotificationQueue.dequeue(chunk_size)
    for message in chunk(dequeue, chunk_size):
        for sender in senders:
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
