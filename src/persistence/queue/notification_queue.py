import json

from peewee import IntegerField, CharField, DateTimeField
from pendulum import datetime, now
from playhouse.postgres_ext import JSONField

from src.persistence import BaseModel
from src.persistence import database_


class NotificationQueue(BaseModel):
    """ Notification Queue DB Model """

    id: int = IntegerField(index=True)
    status: int = IntegerField(default=0, null=False)
    try_count: int = IntegerField(default=0, null=False)
    max_tries: int = IntegerField(default=3, null=False)
    checksum: str = CharField(max_length=200)
    payload: int = JSONField(default='{}')

    created_at: datetime = DateTimeField(default=now())
    updated_at: datetime = DateTimeField(default=now())
    priority: int = IntegerField(default=0, null=False)

    class Meta:
        table_name = 'notification_queue'
        table_settings = 'PARTITION BY RANGE (created_at)'

    @classmethod
    def enqueue(cls, queue_checksum: str, message: dict):
        cls.insert(
            checksum=queue_checksum,
            playload=json.dumps(message)
        )

    @classmethod
    def dequeue(cls):
        return cls.select().for_update("FOR UPDATE SKIP LOCKED")


# class NotificationQueue1(NotificationQueue):
#     class Meta:
#         table_name = f'notification_queue_{now().date()}'


if __name__ == "__main__":
    # init_pg()
    def format(date) -> str:
        return date.format("YYYY_MM_DD")


    now = now()
    tmr = now.add(days=1)

    h = database_.create_tables([NotificationQueue])

    database_.execute_sql(
        f"create table notification_queue_{format(now)} partition of notification_queue FOR VALUES FROM ('{now.date()}') TO ('{tmr.date()}')"
    )
