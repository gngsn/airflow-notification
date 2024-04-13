def run():
    from src.domain.message.generator import MessageQueue
    while MessageQueue.has_next():
        print("Message: ", MessageQueue.pop())
