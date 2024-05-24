from peewee import IntegerField, TimestampField, CharField
from pendulum import datetime, now
from playhouse.postgres_ext import JSONField

from src.persistence import BaseModel


class BaseQueue(BaseModel):
    """ Base Queue DB Model """

    class Meta:
        table_name = 'base_queue'

    id: int = IntegerField(primary_key=True)
    status: int = IntegerField(default=0, null=False)
    try_count: int = IntegerField(default=0, null=False)
    max_tries: int = IntegerField(default=3, null=False)
    checksum: str = CharField(max_length=200)
    payload: int = JSONField(default='{}')

    created_at: datetime = TimestampField(default=now())
    updated_at: datetime = TimestampField(default=now())
    priority: int = IntegerField(default=0, null=False)
