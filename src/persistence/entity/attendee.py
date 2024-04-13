from peewee import IntegerField, BooleanField, TimestampField
from pendulum import datetime, now

from src.persistence.base.connection import BaseModel


class Attendee(BaseModel):
    """ Attendee DB Model """

    class Meta:
        table_name = 'attendee'

    meeting_id: int = IntegerField(primary_key=True)
    user_id: int = IntegerField(primary_key=True)

    allowed: bool = BooleanField(default=False)

    updated_at: datetime = TimestampField(default=now())
