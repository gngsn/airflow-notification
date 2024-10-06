from peewee import CharField, AutoField
from playhouse.postgres_ext import JSONField

from src.persistence.base.connection import BaseModel


class MessageSchema(BaseModel):
    """ Message schema DB Model. """

    class Meta:
        table_name = 'message_schema'

    id: str = AutoField(primary_key=True)
    template_id: str = CharField(max_length=50)
    schedule: str = CharField(max_length=255)
    args: dict = JSONField(default={})

    target_db: str = CharField()
    target_items: str = CharField()
    target_users: str = CharField()

    check_keys: str = CharField(max_length=255)

    @classmethod
    def select_all(cls):
        return cls.select()

    def get_targets(self):
        return self.target_items
