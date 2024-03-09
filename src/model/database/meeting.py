from peewee import DateTimeField, CharField, IntegerField
from pendulum import datetime, now

from src.model.database.base import BaseModel


class Meeting(BaseModel):
    """ Meeting DB Model """

    class Meta:
        table_name = 'meeting'

    id: int = IntegerField(primary_key=True)
    room: str = CharField()
    owner: str = CharField()
    start_time: datetime = DateTimeField(default=now())
    end_time: datetime = DateTimeField(default=now())
    updated_at: datetime = DateTimeField(default=now())
    # participants: str # TODO
