import json

from peewee import IntegerField, CharField, DateTimeField, CompositeKey, BigIntegerField
from pendulum import datetime, now, date
from playhouse.postgres_ext import JSONField

from src.persistence import BaseModel, execute

NOTIFICATION_QUEUE_TABLE_NAME = 'notification_queue'
PARTITION_FORMAT = "YYYY_MM_DD"


class NotificationQueue(BaseModel):
    """ Notification Queue DB Model """

    id: int = BigIntegerField()
    status: int = IntegerField(default=0, null=False)
    try_count: int = IntegerField(default=0, null=False)
    max_tries: int = IntegerField(default=3, null=False)
    key: str = CharField(max_length=200)
    payload: int = JSONField(default='{}')

    created_at: datetime = DateTimeField(default=now())
    updated_at: datetime = DateTimeField(default=now())
    priority: int = IntegerField(default=0, null=False)

    class Meta:
        table_name = NOTIFICATION_QUEUE_TABLE_NAME
        primary_key = CompositeKey('id', 'created_at')
        indexes = (
            # Unique Key
            # -  Indexes 아이템 개수가 하나일 때 반드시 trailing comma 를 붙여주어야 함
            (('checksum', 'created_at'), True),
        )
        table_settings = 'PARTITION BY RANGE (created_at)'

    @classmethod
    def enqueue(cls, key: str, message: dict):
        cls.insert(key=key, payload=json.dumps(message)).execute()

    @classmethod
    def dequeue(cls, offset, chunk):
        return cls.select().where(cls.status == 0).offset(offset).limit(chunk).for_update("FOR UPDATE SKIP LOCKED")

    @classmethod
    def update_success_done(cls, id):
        where = cls.update(try_account=cls.try_count + 1, status=1, updated_at=now()).where(cls.id == id)
        return where.execute()

    @classmethod
    def update_failure_done(cls, id):
        where = cls.update(try_account=cls.try_count + 1, status=-1, updated_at=now()).where(cls.id == id)
        return where.execute()

    @classmethod
    def get_partition_name(cls, now_date: date):
        formatted_date = now_date.format(PARTITION_FORMAT)

        return f"{NOTIFICATION_QUEUE_TABLE_NAME}_{format(formatted_date)}"

    @classmethod
    def create_partition_if_not_exists(cls, now_date=now().date()):
        table_name = NOTIFICATION_QUEUE_TABLE_NAME
        partition_name = NotificationQueue.get_partition_name(now_date)

        if is_exist_partition(table_name, partition_name):
            return

        execute(f"""
            CREATE TABLE {partition_name}
            PARTITION OF {table_name}
            FOR VALUES FROM ('{now_date}') TO ('{now_date.add(days=1)}')""")


def is_exist_partition(table_name, partition_name):
    cursor = execute(f"""
            SELECT
                parent.relname      AS parent,
                child.relname       AS child
            FROM pg_inherits
                JOIN pg_class parent            ON pg_inherits.inhparent = parent.oid
                JOIN pg_class child             ON pg_inherits.inhrelid   = child.oid
            WHERE parent.relname='{table_name}' and child.relname='{partition_name}';
        """)

    return cursor.rowcount != 0


if __name__ == "__main__":
    now = datetime(year=2024, month=5, day=23, hour=13, minute=13)

    NotificationQueue.enqueue(
        "UMSV10001:12",
        {"message": "hello world", "user_id": 12},
    )

    dequeue = NotificationQueue.dequeue()

    print(dequeue)
    for message in dequeue:
        print(message)

if __name__ == "__main__":
    NotificationQueue.create_partition_if_not_exists(date(year=2024, month=5, day=23))
