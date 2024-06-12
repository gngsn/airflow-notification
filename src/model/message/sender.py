from abc import ABC
from typing import Iterator, Callable

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


def do_into_chunk(callback: Callable, size: int):
    while True:
        result = callback(size)

        if result is None:
            break


def run():
    chunk_size = 100
    senders = [ConsoleSender()]
    offset = 0

    while True:
        offset = offset + chunk_size + 1
        code = send(senders, offset, chunk_size)

        if code == -1:
            print("ERROR")
        if code == 0:
            print("Nothing happened")
            break
        if code == 1:
            print("SUCCESS")


def send(senders, offset, limit):
    dequeue = NotificationQueue.dequeue(offset, limit)
    if len(dequeue) == 0:
        return 0

    for message in dequeue:
        for sender in senders:
            code = sender.send(message)
            return code


class Sender(ABC):
    async def send(self, message) -> int:
        raise NotImplementedError()


class ConsoleSender(Sender):
    async def send(self, message) -> int:
        print(message)
        return 1
