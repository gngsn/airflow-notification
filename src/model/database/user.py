from peewee import CharField, AutoField, DateTimeField
from pendulum import datetime, now

from src.model.database.base import BaseModel


class User(BaseModel):
    """ User DB Model """

    class Meta:
        table_name = 'users'

    id: int = AutoField()
    name: str = CharField(max_length=100)
    updated_at: datetime = DateTimeField(default=now())
