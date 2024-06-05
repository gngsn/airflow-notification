from abc import ABC

from src.persistence.queue import NotificationQueue


def run():
    chunk = 10
    dequeue = NotificationQueue.dequeue(chunk)
    senders = [ConsoleSender()]

    print(dequeue)
    for message in dequeue:
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
