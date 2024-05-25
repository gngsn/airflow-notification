import json

from peewee import IntegerField, CharField, DateTimeField
from pendulum import datetime, now, date
from playhouse.postgres_ext import JSONField

from src.persistence import BaseModel

NOTIFICATION_QUEUE_TABLE_NAME = 'notification_queue'
PARTITION_FORMAT = "YYYY_MM_DD"


class NotificationQueue(BaseModel):
    """ Notification Queue DB Model """

    id: int = IntegerField(sequence="notification_queue_seq")
    status: int = IntegerField(default=0, null=False)
    try_count: int = IntegerField(default=0, null=False)
    max_tries: int = IntegerField(default=3, null=False)
    checksum: str = CharField(max_length=200)
    payload: int = JSONField(default='{}')

    created_at: datetime = DateTimeField(default=now())
    updated_at: datetime = DateTimeField(default=now())
    priority: int = IntegerField(default=0, null=False)

    class Meta:
        table_name = NOTIFICATION_QUEUE_TABLE_NAME
        table_settings = 'PARTITION BY RANGE (created_at)'

    @classmethod
    def enqueue(cls, queue_checksum: str, message: dict, **kargs):
        cls.insert(
            checksum=queue_checksum,
            payload=json.dumps(message),
            **kargs
        ).execute()

    @classmethod
    def dequeue(cls):
        return cls.select().for_update("FOR UPDATE SKIP LOCKED")

    @classmethod
    def get_partition_name(cls, now_date: date):
        formatted_date = now_date.format(PARTITION_FORMAT)

        return f"{NOTIFICATION_QUEUE_TABLE_NAME}_{format(formatted_date)}"


if __name__ == "__main__":
    now = datetime(year=2024, month=5, day=23, hour=13, minute=13)

    NotificationQueue.enqueue(
        "UMSV10001:12",
        {"message": "hello world", "user_id": 12},
        created_at=now
    )

    dequeue = NotificationQueue.dequeue()
    
    print(dequeue)
    for message in dequeue:
        print(message)
