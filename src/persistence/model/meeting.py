from peewee import DateTimeField, CharField, IntegerField
from pendulum import datetime, now

from src.persistence.base.connection import BaseModel


class Meeting(BaseModel):
    """ Meeting DB Model """

    class Meta:
        table_name = 'meeting'

    id: int = IntegerField(primary_key=True)
    name: str = CharField(max_length=255)
    room: str = CharField(max_length=31)
    owner: str = CharField(max_length=255)  # TODO: Normalization
    start_time: datetime = DateTimeField(default=now())
    end_time: datetime = DateTimeField(default=now())
    updated_at: datetime = DateTimeField(default=now())
