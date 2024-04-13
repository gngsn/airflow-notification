def run():
    from src.model.message.generator import MessageQueue
    while MessageQueue.has_next():
        print("Message: ", MessageQueue.pop())
