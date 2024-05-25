from src.persistence.queue import NotificationQueue


def run():
    dequeue = NotificationQueue.dequeue()

    print(dequeue)
    for message in dequeue:
        print(message)
