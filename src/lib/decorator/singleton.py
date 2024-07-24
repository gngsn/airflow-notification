import threading


def singleton(cls):
    instances = {}
    lock = threading.Lock()

    def get_instance(*args, **kwargs):
        if cls not in instances:
            with lock:
                instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return get_instance