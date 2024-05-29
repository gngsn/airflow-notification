from src.persistence import database_, init_pg
from src.persistence.queue import NotificationQueue

pg_url = "postgresql://postgres:postgres@localhost/test_ums"


def test_create_notification_queue():
    init_pg(pg_url)
    database_.create_tables([NotificationQueue])


def test_is_exist_partition():
    assert False
