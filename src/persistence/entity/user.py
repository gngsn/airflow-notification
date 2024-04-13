from peewee import CharField, AutoField, TimestampField
from pendulum import datetime, now

from src.persistence.base.connection import BaseModel


class User(BaseModel):
    """ User DB Model """

    class Meta:
        table_name = 'users'

    id: int = AutoField()
    first_name: str = CharField(max_length=100)
    last_name: str = CharField(max_length=100)
    email: str = CharField(max_length=500)
    gender: str = CharField(max_length=50)
    ip_address: str = CharField(max_length=20)

    created_at: datetime = TimestampField(default=now())
    updated_at: datetime = TimestampField(default=now())
