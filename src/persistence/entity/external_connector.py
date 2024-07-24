from peewee import CharField, IntegerField

from src.persistence.base.connection import BaseModel
from src.persistence.entity.schema import MessageSchema


class ExternalDbConnection(BaseModel):
    """External DB Connection Model."""

    class Meta:
        table_name = 'db_connection'

    id: str = CharField(primary_key=True)
    dbms: str = CharField(max_length=50)
    host: str = CharField(max_length=255)
    database: str = CharField(max_length=100)
    port: int = IntegerField()
    username: str = CharField(max_length=100)
    password: str = CharField(max_length=255)

    @classmethod
    def get_target_db_connection(cls, schema: MessageSchema):
        return ExternalDbConnection.get(schema.target_db == ExternalDbConnection.id)

    @classmethod
    def select_all(cls):
        return cls.select()
