from src.lib.decorator.singleton import singleton


@singleton
class SingletonPrinter:
    """
        Singleton
        Hedwig 메세지 전송 담당 Hook - Formatting / Calling API
    """

    def __new__(cls, *args, **kwargs):
        print("__new__ is called\n")
        instance = super().__new__(cls)
        return instance

    def __init__(self, name):
        self.name = name
        print("__init__ is called\n")

    def print(self):
        print(f"Hi hi I'm {self.name}")


def _process(num):
    SingletonPrinter(f"싱글톤 테스트 {num}").print()


def test_singleton_multiprocessing():
    from multiprocessing import Pool

    with Pool(5) as p:
        p.map(_process, range(1, 100))


def test_singleton():
    printers = [
        SingletonPrinter("싱글톤 테스트 1"),
        SingletonPrinter("싱글톤 테스트 2"),
        SingletonPrinter("싱글톤 테스트 3")
    ]

    for p in printers:
        print(p.print())
